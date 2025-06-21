import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from server.configuration.environment import SETTINGS
from server.controller.server_controller import router as ping_router
from server.controller.to_do_controller import router as to_do_router
from server.utils.handler import setup_marketplace_exception_handling
from server.utils.logger import logger


def init_app() -> FastAPI:
    return _init_fast_api_app()


def _init_fast_api_app() -> FastAPI:
    logger.info("Starting To-Do API application...")
    app = FastAPI(**_get_app_args())
    app = _config_app_routes(app)
    app = _config_app_exceptions(app)
    app = _config_app_middlewares(app)
    app.openapi = lambda: _custom_openapi(app)
    setup_marketplace_exception_handling(app)
    return app


def _config_app_routes(app: FastAPI) -> FastAPI:
    routers = [
        # Importar os routers aqui
        ping_router,
        to_do_router,
    ]
    for route in routers:
        app.include_router(route)
    return app


def _get_app_args() -> dict:
    return dict(
        title="To-Do API",
        description="ToDo API",
        # root_path=SETTINGS.root_path,
        version=SETTINGS.version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )


def _custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="To-Do API",
        version="1.0.0",
        description="To-Do API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def _config_app_exceptions(app: FastAPI) -> FastAPI:
    app = _config_validation_exceptions(app)
    app = _config_http_exceptions(app)
    return app


def _config_validation_exceptions(app: FastAPI) -> FastAPI:
    # add_exception_handlers(app)
    return app


def _config_http_exceptions(app: FastAPI) -> FastAPI:
    # add_http_exception_handlers(app)
    return app


def _config_app_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:4200")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
