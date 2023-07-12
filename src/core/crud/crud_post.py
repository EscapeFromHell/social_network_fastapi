from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.crud import CRUDBase
from src.core.models import Post
from src.core.schemas import Post as PostSchema
from src.core.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_all_posts(self, db: Session) -> List[Post]:
        """
        Get all posts from the database.

        :param db: Session - SQLAlchemy database session.
        :return: List[Post] - List of post objects.
        """
        posts = db.query(Post).order_by(desc(Post.id)).all()
        return [
            PostSchema(
                id=post.id,
                text=post.text,
                author=post.author.username,
                publication_date=post.publication_date,
                likes=post.likes,
                dislikes=post.dislikes,
            )
            for post in posts
        ]

    def add_like(self, db: Session, post: Post) -> None:
        """
        Increment the like count of a post and commit the changes to the database.

        :param db: Session - SQLAlchemy database session.
        :param post: Post - Post object to update.
        :return: None
        """
        post.likes += 1
        db.commit()

    def remove_like(self, db: Session, post: Post) -> None:
        """
        Decrement the like count of a post and commit the changes to the database.

        :param db: Session - SQLAlchemy database session.
        :param post: Post - Post object to update.
        :return: None
        """
        post.likes -= 1
        db.commit()

    def add_dislike(self, db: Session, post: Post) -> None:
        """
        Increment the dislike count of a post and commit the changes to the database.

        :param db: Session - SQLAlchemy database session.
        :param post: Post - Post object to update.
        :return: None
        """
        post.dislikes += 1
        db.commit()

    def remove_dislike(self, db: Session, post: Post) -> None:
        """
        Decrement the dislike count of a post and commit the changes to the database.

        :param db: Session - SQLAlchemy database session.
        :param post: Post - Post object to update.
        :return: None
        """
        post.dislikes -= 1
        db.commit()


crud_post = CRUDPost(Post)
