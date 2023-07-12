from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUDBase class.

        :param model: Type[ModelType] - SQLAlchemy model type.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single object from the database.

        :param db: Session - SQLAlchemy database session.
        :param id: Any - Identifier of the object.
        :return: Optional[ModelType] - Object if found, None otherwise.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create an object in the database.

        :param db: Session - SQLAlchemy database session.
        :param obj_in: CreateSchemaType - Object creation input data.
        :return: ModelType - Created object.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        Update an object in the database.

        :param db: Session - SQLAlchemy database session.
        :param db_obj: ModelType - Object to update.
        :param obj_in: Union[UpdateSchemaType, Dict[str, Any]] - Object update input data.
        :return: ModelType - Updated object.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Remove an object from the database.

        :param db: Session - SQLAlchemy database session.
        :param id: int - Identifier of the object to remove.
        :return: ModelType - Removed object.
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
