from app.routers.auth import router as auth_router
from app.routers.assistant import router as assistant_router
from app.routers.friends import router as friends_router
from app.routers.interactions import router as interactions_router
from app.routers.posts import router as posts_router
from app.routers.stats import router as stats_router
from app.routers.upload import router as upload_router
from app.routers.users import router as users_router

__all__ = [
    "auth_router",
    "assistant_router",
    "posts_router",
    "interactions_router",
    "upload_router",
    "users_router",
    "friends_router",
    "stats_router",
]
