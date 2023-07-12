from sqlalchemy import Column, Date, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.models.base import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    publication_date = Column(Date, default=func.now())
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    reactions = relationship("Reaction", back_populates="post")
