"""Main application for the User Service."""

from contextlib import asynccontextmanager
from typing import Annotated

from ab_core.alembic_auto_migrate.service import AlembicAutoMigrate
from ab_core.dependency import Depends, inject
from ab_core.logging.config import LoggingConfig
from fastapi import FastAPI

from ab_service.bff.routes.auth import router as auth_router
from ab_service.bff.routes.identity_context import router as identity_context_router
from ab_service.bff.routes.token_issuer import router as token_issuer_router

from .dependencies import (
    AuthClient,
    Database,
    TokenIssuerClient,
    TokenIssuerStoreClient,
    TokenStoreClient,
    TokenValidatorClient,
    UserClient,
    get_auth_client,
    get_database,
    get_token_issuer_client,
    get_token_issuer_store_client,
    get_token_store_client,
    get_token_validator_client,
    get_user_client,
)


@asynccontextmanager
@inject
async def lifespan(
    _app: FastAPI,
    _db: Annotated[
        Database,
        Depends(
            get_database,
            persist=True,
        ),
    ],  # cold start load db into cache
    logging_config: Annotated[
        LoggingConfig,
        Depends(
            LoggingConfig,
            persist=True,
        ),
    ],
    alembic_auto_migrate: Annotated[
        AlembicAutoMigrate,
        Depends(
            AlembicAutoMigrate,
            persist=True,
        ),
    ],
    _auth_client: Annotated[
        AuthClient,
        Depends(
            get_auth_client,
            persist=True,
        ),
    ],
    _token_validator_client: Annotated[
        TokenValidatorClient,
        Depends(
            get_token_validator_client,
            persist=True,
        ),
    ],
    _user_client: Annotated[
        UserClient,
        Depends(
            get_user_client,
            persist=True,
        ),
    ],
    _token_issuer_client: Annotated[
        TokenIssuerClient,
        Depends(
            get_token_issuer_client,
            persist=True,
        ),
    ],
    _token_issuer_store_client: Annotated[
        TokenIssuerStoreClient,
        Depends(
            get_token_issuer_store_client,
            persist=True,
        ),
    ],
    _token_store_client: Annotated[
        TokenStoreClient,
        Depends(
            get_token_store_client,
            persist=True,
        ),
    ],
):
    """Lifespan context manager to handle startup and shutdown events."""
    logging_config.apply()
    alembic_auto_migrate.run()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(identity_context_router)
app.include_router(token_issuer_router)
