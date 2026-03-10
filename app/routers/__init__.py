from app.routers.alerts_router import router as alerts_router
from app.routers.auth_router import router as auth_router
from app.routers.incidents_router import router as incidents_router
from app.routers.users_router import router as users_router

__all__ = ["auth_router", "users_router", "alerts_router", "incidents_router"]

