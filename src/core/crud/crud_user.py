from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from src.config import get_password_hash
from src.core.crud import CRUDBase
from src.core.models import User
from src.core.schemas import ExtraUserFields, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Get a user by username from the database.

        :param db: Session - SQLAlchemy database session.
        :param username: str - Username of the user.
        :return: Optional[User] - User object if found, None otherwise.
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get a user by email from the database.

        :param db: Session - SQLAlchemy database session.
        :param email: str - Email of the user.
        :return: Optional[User] - User object if found, None otherwise.
        """
        return db.query(User).filter(User.email == email).first()

    def add_user(self, db: Session, obj_in: UserCreate, extra_fields: Optional[ExtraUserFields]) -> User:
        """
        Add a new user to the database.

        :param db: Session - SQLAlchemy database session.
        :param obj_in: UserCreate - User creation input data.
        :param extra_fields: Optional[ExtraUserFields] - Extra user fields (name, surname).
        :return: User - User object created in the database.
        """
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        if extra_fields:
            db_obj.name = extra_fields.name
            db_obj.surname = extra_fields.surname

        db.add(db_obj)
        db.commit()
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        """
        Update a user in the database.

        :param db: Session - SQLAlchemy database session.
        :param db_obj: User - User object to update.
        :param obj_in: Union[UserUpdate, Dict[str, Any]] - User update input data.
        :return: User - Updated User object.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_user = CRUDUser(User)
