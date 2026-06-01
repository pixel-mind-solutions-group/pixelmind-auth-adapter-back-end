from fastapi import Request
from fastapi.responses import JSONResponse
from .custom_exceptions import AppException


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
