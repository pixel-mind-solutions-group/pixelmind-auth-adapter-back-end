import logging

from fastapi import FastAPI
from core.database import Base, engine
from exceptions.handlers import register_exception_handlers
from routers.user.user_router import router as user_router
from routers.application.application_router import router as application_router
from routers.realm.realm_router import router as realm_router
from routers.module.module_router import router as module_router
from routers.api_permission.api_permission_router import router as api_permission_router
from routers.application_has_api_permission.application_has_api_permission_router import (
    router as application_has_api_permission_router,
)
from routers.ui_permission.ui_permission_router import router as ui_permission_router
from routers.application_has_ui_permission.application_has_ui_permission_router import (
    router as application_has_ui_permission_router,
)
from routers.module_has_api_permission.module_has_api_permission_router import (
    router as module_has_api_permission_router,
)
from routers.module_has_ui_permission.module_has_ui_permission_router import (
    router as module_has_ui_permission_router,
)
from utils.migration import run_auto_migrations
import configs.logging_config  # logging enabled
from configs.cors_config import register_cors  # CORS enabled

app = FastAPI(
    title="Pixel Auth Adapter API",
    description="API for Pixel Auth Adapter",
    version="1.0.0",
)

# RUN DATABASE AUTO-MIGRATIONS ON STARTUP
run_auto_migrations()

app.include_router(user_router)
app.include_router(application_router)
app.include_router(realm_router)
app.include_router(module_router)
app.include_router(api_permission_router)
app.include_router(application_has_api_permission_router)
app.include_router(ui_permission_router)
app.include_router(application_has_ui_permission_router)
app.include_router(module_has_api_permission_router)
app.include_router(module_has_ui_permission_router)


register_exception_handlers(app)

register_cors(app)


@app.get("/")
def home():
    return {"message": "Pixel Auth Adapter Application Running Successfully"}
