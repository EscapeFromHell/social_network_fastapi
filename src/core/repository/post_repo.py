from typing import List

from fastapi import HTTPException

from src.core.crud import crud_post, crud_reaction
from src.core.models import Post as PostModel
from src.core.models import Reaction as ReactionModel
from src.core.repository.repository import Repository
from src.core.schemas import Post, PostCreate, PostResponseMessage, PostUpdate, User


class PostRepo(Repository):
    def __get_post(self, post_id: int) -> PostModel:
        """
        Get the post from the database by ID.

        :param post_id: int - Post ID.
        :return: PostModel - Retrieved post.
        """
        post = crud_post.get(db=self.db, id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with ID: {post_id} not found")
        return post

    async def show_posts(self) -> List[Post]:
        """
        Get all posts.

        :return: List[Post] - List of posts.
        """
        return crud_post.get_all_posts(db=self.db)

    async def create_post(self, obj_in: PostCreate) -> Post:
        """
        Create a new post.

        :param obj_in: PostCreate - Post creation data.
        :return: Post - Created post.
        """
        post = crud_post.create(db=self.db, obj_in=obj_in)
        return Post(
            id=post.id,
            text=post.text,
            author=post.author.username,
            publication_date=post.publication_date,
            likes=post.likes,
            dislikes=post.dislikes,
        )

    async def edit_post(self, obj_in: PostUpdate, post_id: int, current_user: User) -> Post:
        """
        Edit an existing post.

        :param obj_in: PostUpdate - Updated post data.
        :param post_id: int - Post ID.
        :param current_user: User - Current user making the request.
        :return: Post - Updated post.
        """
        post = self.__get_post(post_id=post_id)
        if post.author.username != current_user.username:
            raise HTTPException(status_code=403, detail="Access denied. You can only modify your own posts.")

        post = crud_post.update(db=self.db, db_obj=post, obj_in=obj_in)
        return Post(
            id=post.id,
            text=post.text,
            author=post.author.username,
            publication_date=post.publication_date,
            likes=post.likes,
            dislikes=post.dislikes,
        )

    async def delete_post(self, post_id: int, current_user: User) -> PostResponseMessage:
        """
        Delete a post.

        :param post_id: int - Post ID.
        :param current_user: User - Current user making the request.
        :return: PostResponseMessage - Response message.
        """
        post = self.__get_post(post_id=post_id)
        if post.author.username != current_user.username:
            raise HTTPException(status_code=403, detail="Access denied. You can only delete your own posts.")

        crud_post.remove(db=self.db, id=post_id)
        return PostResponseMessage(message=f"Post with ID: {post_id} successfully deleted")

    def __change_like(self, existing_reaction: ReactionModel, post: PostModel, user_id: int):
        """
        Change a like reaction for a post.

        :param existing_reaction: ReactionModel - Existing reaction.
        :param post: PostModel - Post model.
        :param user_id: int - User ID.
        :return: PostResponseMessage - Response message.
        """
        if existing_reaction.reaction_type == "like":
            crud_reaction.remove(db=self.db, id=existing_reaction.id)
            crud_post.remove_like(db=self.db, post=post)
            return PostResponseMessage(message="Like removed successfully")

        if existing_reaction.reaction_type == "dislike":
            crud_reaction.remove(db=self.db, id=existing_reaction.id)
            crud_post.remove_dislike(db=self.db, post=post)
            crud_reaction.add_reaction(db=self.db, post_id=post.id, user_id=user_id, reaction_type="like")
            crud_post.add_like(db=self.db, post=post)
            return PostResponseMessage(message="Reaction changed successfully: Dislike replaced with Like.")

    def __change_dislike(self, existing_reaction: ReactionModel, post: PostModel, user_id: int):
        """
        Change a dislike reaction for a post.

        :param existing_reaction: ReactionModel - Existing reaction.
        :param post: PostModel - Post model.
        :param user_id: int - User ID.
        :return: PostResponseMessage - Response message.
        """
        if existing_reaction.reaction_type == "dislike":
            crud_reaction.remove(db=self.db, id=existing_reaction.id)
            crud_post.remove_dislike(db=self.db, post=post)
            return PostResponseMessage(message="Dislike removed successfully")

        if existing_reaction.reaction_type == "like":
            crud_reaction.remove(db=self.db, id=existing_reaction.id)
            crud_post.remove_like(db=self.db, post=post)
            crud_reaction.add_reaction(db=self.db, post_id=post.id, user_id=user_id, reaction_type="dislike")
            crud_post.add_dislike(db=self.db, post=post)
            return PostResponseMessage(message="Reaction changed successfully: Like replaced with Dislike.")

    async def like_post(self, post_id: int, current_user: User) -> PostResponseMessage:
        """
        Like a post.

        :param post_id: int - Post ID.
        :param current_user: User - Current user making the request.
        :return: PostResponseMessage - Response message.
        """
        post = self.__get_post(post_id=post_id)
        if post.author.username == current_user.username:
            raise HTTPException(status_code=400, detail="You cannot like your own post")

        existing_reaction = crud_reaction.get_reaction(db=self.db, post_id=post_id, user_id=current_user.id)
        if existing_reaction:
            return self.__change_like(existing_reaction=existing_reaction, post=post, user_id=current_user.id)

        crud_reaction.add_reaction(db=self.db, post_id=post_id, user_id=current_user.id, reaction_type="like")
        crud_post.add_like(db=self.db, post=post)
        return PostResponseMessage(message="Post liked successfully")

    async def dislike_post(self, post_id: int, current_user: User) -> PostResponseMessage:
        """
        Dislike a post.

        :param post_id: int - Post ID.
        :param current_user: User - Current user making the request.
        :return: PostResponseMessage - Response message.
        """
        post = self.__get_post(post_id=post_id)
        if post.author.username == current_user.username:
            raise HTTPException(status_code=400, detail="You cannot dislike your own post")

        existing_reaction = crud_reaction.get_reaction(db=self.db, post_id=post_id, user_id=current_user.id)
        if existing_reaction:
            return self.__change_dislike(existing_reaction=existing_reaction, post=post, user_id=current_user.id)

        crud_reaction.add_reaction(db=self.db, post_id=post_id, user_id=current_user.id, reaction_type="dislike")
        crud_post.add_dislike(db=self.db, post=post)
        return PostResponseMessage(message="Post disliked successfully")
