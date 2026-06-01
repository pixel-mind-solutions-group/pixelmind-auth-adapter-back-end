import logging

from fastapi import FastAPI
from core.database import Base, engine
from exceptions.handlers import register_exception_handlers
from routers.user.user_router import router as user_router
import configs.logging_config  # logging enabled
from configs.cors_config import register_cors  # CORS enabled

app = FastAPI(
    title="Pixel Auth Adapter API",
    description="API for Pixel Auth Adapter",
    version="1.0.0",
)

# CREATE TABLES (ONLY ONCE)
Base.metadata.create_all(bind=engine)

app.include_router(user_router)

register_exception_handlers(app)

register_cors(app)


@app.get("/")
def home():
    return {"message": "Pixel Auth Adapter Application Running Successfully"}
