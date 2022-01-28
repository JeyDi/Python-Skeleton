from typing import Any
import uvicorn
from fastapi import FastAPI, responses
from starlette.middleware.cors import CORSMiddleware


from app.src.logger import logger
from app.src.api.api import api_router
from app.src.config import settings
from app.src.db.initialize import initialization

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def on_startup():
    """Initialize the database with the tables"""
    initialization()


@app.get("/")
def start_screen() -> Any:
    """
    Startup route
    """
    url_swagger = f"http://{settings.API_ENDPOINT_HOST}:{settings.APP_DOCKER_PORT}/docs"
    url_redoc = f"http://{settings.API_ENDPOINT_HOST}:{settings.APP_DOCKER_PORT}/redoc"
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to: JeyDi FastAPI Template</h1>"
        "<ul>"
        f"<li><a href={url_swagger}>Link to the Swagger documentation</a></li>"
        f"<li><a href={url_redoc}>Link to the Redoc documentation</a></li>"
        "</ul>"
        "</body>"
        "</html>"
    )
    return responses.HTMLResponse(content=body)


if __name__ == "__main__":
    if settings.DEBUG_MODE:
        logger.debug(f"Launching the app in debug mode: {settings.DEBUG_MODE}")
        uvicorn.run(
            app, port=settings.API_ENDPOINT_PORT, host=settings.API_ENDPOINT_HOST
        )
