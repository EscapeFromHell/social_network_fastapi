from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, constr

from src.core.clients import UserClient
from src.core.repository import AuthRepo
from src.core.schemas import SuccessAuth, SuccessSignUp, User, UserCreate
from src.deps import auth_repo as deps_auth_repo
from src.deps import get_current_user as deps_get_current_user
from src.deps import user_client as deps_user_client

router = APIRouter()


@router.post("/signup", response_model=SuccessSignUp, status_code=201)
async def signup(
    *,
    username: constr(min_length=4, max_length=20),
    password: constr(min_length=6),
    email: EmailStr,
    auth_repo: AuthRepo = Depends(deps_auth_repo),
    user_client: UserClient = Depends(deps_user_client),
) -> SuccessSignUp:
    """
    Register a new user.

    :param username: str - Username (min length: 4, max length: 20)
    :param password: str - Password (min length: 6)
    :param email: EmailStr - Email address
    :param auth_repo: AuthRepo - repository for handling authentication and authorization operations
    :param user_client: UserClient - client for checking user's email
    :return: SuccessSignUp - user information
    """
    return await auth_repo.signup(
        user_in=UserCreate(username=username, email=email, password=password), user_client=user_client
    )


@router.post("/login", status_code=200, response_model=SuccessAuth)
async def login(
    *, auth_repo: AuthRepo = Depends(deps_auth_repo), form_data: OAuth2PasswordRequestForm = Depends()
) -> SuccessAuth:
    """
    Generate an access token.

    :param auth_repo: AuthRepo - repository for handling authentication and authorization operations
    :param form_data: OAuth2PasswordRequestForm - form data for authentication
    :return: SuccessAuth - access token for login
    """
    return await auth_repo.login(form_data=form_data)


@router.get("/me", status_code=200, response_model=User)
def current_user_profile(current_user: User = Depends(deps_get_current_user)) -> User:
    """
    Fetch the current logged-in user profile.

    :param current_user: User
    :return Current user profile: User
    """
    return current_user
