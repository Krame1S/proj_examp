from fastapi import APIRouter

from gateway.api.v1.attachments import router as attachments_router
from gateway.api.v1.auth import router as auth_router
from gateway.api.v1.categories import router as category_router
from gateway.api.v1.comments import router as comments_router
from gateway.api.v1.dashboard import router as dashboard_router
from gateway.api.v1.health import router as health_router
from gateway.api.v1.tags import router as tags_router
from gateway.api.v1.tasks import router as tasks_router
from gateway.api.v1.users import router as users_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(health_router)
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(tasks_router)
v1_router.include_router(category_router)
v1_router.include_router(tags_router)
v1_router.include_router(comments_router)
v1_router.include_router(attachments_router)
v1_router.include_router(dashboard_router)
