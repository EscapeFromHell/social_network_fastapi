from sqlalchemy import Column, Date, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.models.base import Base


class Reaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    reaction_type = Column(String)
    user = relationship("User", back_populates="reactions")
    post = relationship("Post", back_populates="reactions")
