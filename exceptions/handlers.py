import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .custom_exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app):

    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "status": exc.status_code,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(request: Request, exc: RequestValidationError):
        error_details = []
        for error in exc.errors():
            loc_path = ".".join(str(loc) for loc in error.get("loc", [])[1:])
            msg = error.get("msg", "Invalid value")
            error_details.append(f"{loc_path}: {msg}")
        
        message = "Validation Error: " + "; ".join(error_details)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": message,
                "status": 400,
            },
        )

    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        if isinstance(exc, StarletteHTTPException):
            return await http_exception_handler(request, exc)
        if isinstance(exc, RequestValidationError):
            return await handle_validation_exception(request, exc)

        logger.error(f"Unhandled Internal Server Error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "status": 500,
            },
        )
