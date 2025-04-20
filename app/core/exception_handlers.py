from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logger import logger


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, StarletteHTTPException):
        return await global_exception_handler(request, exc)

    status = exc.status_code
    detail = exc.detail
    logger.warning("HTTPException", path=str(request.url), detail=detail)
    return JSONResponse(status_code=status, content={"error": detail})


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        return await global_exception_handler(request, exc)

    errors = exc.errors()
    logger.warning("RequestValidationError", path=str(request.url), errors=errors)
    return JSONResponse(status_code=422, content={"errors": errors})


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled Exception", path=str(request.url), error=str(exc))
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
