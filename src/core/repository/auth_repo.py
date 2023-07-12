from datetime import datetime, timedelta
from typing import List, MutableMapping, Union

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import EmailStr

from src.config import settings, verify_password
from src.core.clients import UserClient
from src.core.crud import crud_user
from src.core.models import User
from src.core.repository.repository import Repository
from src.core.schemas import SuccessAuth, SuccessSignUp, UserCreate


class AuthRepo(Repository):
    JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]

    def __create_token(self, token_type: str, lifetime: timedelta, user_id: int) -> str:
        """Create a JWT token with the specified token type, lifetime, and user ID.

        :param token_type: str - the type of the token
        :param lifetime: timedelta - the lifetime of the token
        :param user_id: int - the ID of the user
        :return: str - the encoded JWT token
        """
        payload = {}
        expire = datetime.utcnow() + lifetime
        payload["type"] = token_type

        # The "exp" (expiration time) claim identifies the expiration time on
        # or after which the JWT MUST NOT be accepted for processing
        payload["exp"] = expire

        # The "iat" (issued at) claim identifies the time at which the
        # JWT was issued.
        payload["iat"] = datetime.utcnow()

        # The "sub" (subject) claim identifies the principal that is the
        # subject of the JWT
        payload["sub"] = str(user_id)
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    def __create_access_token(self, user_id: int) -> str:
        """
        Create an access token for the specified user ID.

        :param user_id: int - the ID of the user
        :return: str - the encoded access token
        """
        return self.__create_token(
            token_type="access_token",
            lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            user_id=user_id,
        )

    def __check_username(self, username: str) -> bool:
        """
        Check if the username is already taken.

        :param username: str - the username to check
        :return: bool - True if the username is available
        """
        user = crud_user.get_by_username(db=self.db, username=username)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system",
            )
        return True

    async def __check_email(self, email: EmailStr, user_client: UserClient) -> bool:
        """
        Check if the email is already registered and verify its existence.

        :param email: EmailStr - the email to check
        :param user_client: UserClient - the user client to perform email verification
        :return: bool - True if the email is available and verified
        """
        user = crud_user.get_by_email(db=self.db, email=email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        verification = await user_client.email_verifier(email=email)
        if verification:
            return True

    def __authenticate(self, username: str, password: str) -> User:
        """
        Authenticate the user with the provided username and password.

        :param username: str - the username
        :param password: str - the password
        :return: User - the authenticated user
        """
        user = crud_user.get_by_username(db=self.db, username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return user

    async def signup(self, user_in: UserCreate, user_client: UserClient) -> SuccessSignUp:
        """
        Register a new user.

        :param user_in: UserCreate - data of the new user
        :param user_client: UserClient - client for checking user's email
        :return: SuccessSignUp - user information
        """
        if self.__check_username(username=user_in.username) and await self.__check_email(
            email=user_in.email, user_client=user_client
        ):
            extra_fields = await user_client.get_additional_data(email=user_in.email)
            user = crud_user.add_user(db=self.db, obj_in=user_in, extra_fields=extra_fields)

            return SuccessSignUp(
                id=user.id, username=user.username, email=user.email, registration_date=user.registration_date
            )

    async def login(self, form_data: OAuth2PasswordRequestForm) -> SuccessAuth:
        """
        Log in the user and generate an access token.

        :param form_data: OAuth2PasswordRequestForm - the form data for authentication
        :return: SuccessAuth - access token for login
        """
        user = self.__authenticate(username=form_data.username, password=form_data.password)
        access_token = self.__create_access_token(user_id=user.id)
        token_type = "bearer"
        return SuccessAuth(access_token=access_token, token_type=token_type)
