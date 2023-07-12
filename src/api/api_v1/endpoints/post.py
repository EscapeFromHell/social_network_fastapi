from typing import List

from fastapi import APIRouter, Body, Depends
from pydantic import PositiveInt

from src.core.repository import PostRepo
from src.core.schemas import Post, PostCreate, PostResponseMessage, PostUpdate, User
from src.deps import get_current_user as deps_get_current_user
from src.deps import post_repo as deps_post_repo

router = APIRouter()


@router.get("/", status_code=200, response_model=List[Post])
async def show_posts(
    *,
    post_repo: PostRepo = Depends(deps_post_repo),
) -> List[Post]:
    """
    Get all posts.

    :param post_repo: PostRepo - Repository for managing posts.
    :return: List[Post] - List of posts.
    """
    return await post_repo.show_posts()


@router.post("/", status_code=201, response_model=Post)
async def create_post(
    *,
    text: str = Body(min_length=1, max_length=560),
    post_repo: PostRepo = Depends(deps_post_repo),
    current_user: User = Depends(deps_get_current_user),
) -> Post:
    """
    Create a new post.

    :param text: str - Text content of the post (min length: 1, max length: 560).
    :param post_repo: PostRepo - Repository for managing posts.
    :param current_user: User - Current logged-in user.
    :return: Post - Created post.
    """
    return await post_repo.create_post(obj_in=PostCreate(text=text, author_id=current_user.id))


@router.put("/", status_code=201, response_model=Post)
async def edit_post(
    *,
    post_id: PositiveInt,
    text: str = Body(min_length=1, max_length=560),
    post_repo: PostRepo = Depends(deps_post_repo),
    current_user: User = Depends(deps_get_current_user),
) -> Post:
    """
    Edit a post.

    :param post_id: int - ID of the post to edit.
    :param text: str - Updated text content of the post (min length: 1, max length: 560).
    :param post_repo: PostRepo - Repository for managing posts.
    :param current_user: User - Current logged-in user.
    :return: Post - Updated post.
    """
    return await post_repo.edit_post(
        obj_in=PostUpdate(text=text, author_id=current_user.id), post_id=post_id, current_user=current_user
    )


@router.delete("/", status_code=200, response_model=PostResponseMessage)
async def delete_post(
    *,
    post_id: PositiveInt,
    post_repo: PostRepo = Depends(deps_post_repo),
    current_user: User = Depends(deps_get_current_user),
) -> PostResponseMessage:
    """
    Delete a post.

    :param post_id: int - ID of the post to delete.
    :param post_repo: PostRepo - Repository for managing posts.
    :param current_user: User - Current logged-in user.
    :return: PostResponseMessage - Success message.
    """
    return await post_repo.delete_post(post_id=post_id, current_user=current_user)


@router.post("/like", status_code=200, response_model=PostResponseMessage)
async def like_post(
    *, post_id: int, post_repo: PostRepo = Depends(deps_post_repo), current_user: User = Depends(deps_get_current_user)
) -> PostResponseMessage:
    """
    Like a post.

    :param post_id: int - ID of the post to like.
    :param post_repo: PostRepo - Repository for managing posts.
    :param current_user: User - Current logged-in user.
    :return: PostResponseMessage - Success message.
    """
    return await post_repo.like_post(post_id=post_id, current_user=current_user)


@router.post("/dislike", status_code=200, response_model=PostResponseMessage)
async def dislike_post(
    *, post_id: int, post_repo: PostRepo = Depends(deps_post_repo), current_user: User = Depends(deps_get_current_user)
) -> PostResponseMessage:
    """
    Dislike a post.

    :param post_id: int - ID of the post to dislike.
    :param post_repo: PostRepo - Repository for managing posts.
    :param current_user: User - Current logged-in user.
    :return: PostResponseMessage - Success message.
    """
    return await post_repo.dislike_post(post_id=post_id, current_user=current_user)
