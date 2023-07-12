from sqlalchemy import Column, Date, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    registration_date = Column(Date, default=func.now())
    posts = relationship(
        "Post",
        cascade="all,delete-orphan",
        back_populates="author",
        uselist=True,
    )
    reactions = relationship("Reaction", back_populates="user")
