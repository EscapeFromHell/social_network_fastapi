from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.config import settings

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH_SCHEME = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the plain password against the hashed password.

    :param plain_password: str - Plain text password.
    :param hashed_password: str - Hashed password.
    :return: bool - True if the plain password matches the hashed password, False otherwise.
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the provided password.

    :param password: str - Plain text password.
    :return: str - Hashed password.
    """
    return PWD_CONTEXT.hash(password)
