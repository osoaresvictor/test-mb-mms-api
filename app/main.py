from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import router
from app.core.exception_handlers import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="Mercado Bitcoin MMS API Test",
    description="""
    Test project about an API that provides simple moving
    averages (MMS) for BRLBTC and BRLETH pairs.
    """,
    version="1.0.0",
    contact={
        "name": "Victor Soares",
        "url": "https://github.com/soares-victor-it",
        "email": "victor_soares@live.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(router)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
