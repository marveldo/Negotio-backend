from fastapi import FastAPI, status, Request , HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError 
from fastapi.responses import JSONResponse
from .logger import logger
from .urls import api_main_route, websocket_main_route
from .settings import settings


app = FastAPI(docs_url=None , redoc_url=None)
app.include_router(api_main_route)
app.include_router(websocket_main_route)

app.mount("/static", StaticFiles(directory=settings.STATIC_FILES), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(RequestValidationError)
async def validation_exception(request: Request, exc: RequestValidationError):
    """Validation exception handler"""

    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "status_code": 422,
            "message": "Invalid input",
            "errors": errors,
        },
    )



@app.exception_handler(HTTPException)
async def http_exception(request: Request, exc: HTTPException):
    """HTTP exception handler"""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )

@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    """Other exception handlers"""

    logger.exception(f"Exception occured; {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "status_code": 500,
            "message": f"An unexpected error occurred: {exc}",
        },
    )

@app.get('/', status_code=status.HTTP_200_OK)
async def home(request : Request):
    return JSONResponse(content={'message' :'Welcome to Fastapi Boilerplate'},status_code=status.HTTP_200_OK)

