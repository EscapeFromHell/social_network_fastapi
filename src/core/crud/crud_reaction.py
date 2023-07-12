from sqlalchemy.orm import Session

from src.core.crud import CRUDBase
from src.core.models import Reaction
from src.core.schemas import ReactionCreate, ReactionUpdate


class CRUDReaction(CRUDBase[Reaction, ReactionCreate, ReactionUpdate]):
    def get_reaction(self, db: Session, post_id: int, user_id: int) -> Reaction:
        """
        Get the reaction for a specific post and user from the database.

        :param db: Session - SQLAlchemy database session.
        :param post_id: int - ID of the post.
        :param user_id: int - ID of the user.
        :return: Reaction - Reaction object if found, None otherwise.
        """
        return db.query(Reaction).filter_by(post_id=post_id, user_id=user_id).first()

    def add_reaction(self, db: Session, post_id: int, user_id: int, reaction_type: str) -> None:
        """
        Add a new reaction to the database.

        :param db: Session - SQLAlchemy database session.
        :param post_id: int - ID of the post.
        :param user_id: int - ID of the user.
        :param reaction_type: str - Type of the reaction.
        :return: None
        """
        reaction = Reaction(post_id=post_id, user_id=user_id, reaction_type=reaction_type)
        db.add(reaction)
        db.commit()


crud_reaction = CRUDReaction(Reaction)
