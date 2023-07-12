from fastapi import APIRouter

from src.api.api_v1.endpoints import auth_router, post_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(post_router, prefix="/posts", tags=["posts"])
