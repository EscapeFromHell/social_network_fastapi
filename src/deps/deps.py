from typing import Generator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config import OAUTH_SCHEME, settings
from src.core.clients import UserClient
from src.core.crud import crud_user
from src.core.db import SessionLocal
from src.core.models import User
from src.core.repository import AuthRepo, PostRepo
from src.core.schemas import TokenData


def get_db() -> Generator:
    """
    Get a database session generator.

    :return: Generator - Database session generator.
    """
    with SessionLocal() as db:
        yield db


def auth_repo(db: Session = Depends(get_db, use_cache=True)) -> AuthRepo:
    """
    Dependency Injection for the AuthRepo repository.

    :param db: Session - Database session.
    :return: AuthRepo - AuthRepo repository instance.
    """
    return AuthRepo(db)


def post_repo(db: Session = Depends(get_db, use_cache=True)) -> PostRepo:
    """
    Dependency Injection for the PostRepo repository.

    :param db: Session - Database session.
    :return: PostRepo - PostRepo repository instance.
    """
    return PostRepo(db)


def user_client() -> UserClient:
    """
    Dependency Injection for the UserClient client.

    :return: UserClient - UserClient client instance.
    """
    return UserClient()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(OAUTH_SCHEME)) -> User:
    """
    Get the current authenticated user.

    :param db: Session - Database session.
    :param token: str - Authentication token.
    :return: User - Current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))

    except JWTError:
        raise credentials_exception

    user = crud_user.get(db=db, id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
