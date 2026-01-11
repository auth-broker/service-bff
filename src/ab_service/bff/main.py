"""Main application for the User Service."""

from contextlib import asynccontextmanager
from typing import Annotated

from ab_client_auth_client.client import Client as AuthClient
from ab_client_token_issuer.client import Client as TokenIssuerClient
from ab_client_token_issuer_store.client import Client as TokenIssuerStoreClient
from ab_client_token_store.client import Client as TokenStoreClient
from ab_client_token_validator.client import Client as TokenValidatorClient
from ab_client_user.client import Client as UserClient
from ab_core.alembic_auto_migrate.service import AlembicAutoMigrate
from ab_core.database.databases import Database
from ab_core.dependency import Depends, inject
from ab_core.logging.config import LoggingConfig
from fastapi import FastAPI

from ab_service.bff.routes.identity_context import router as identity_context_router

from .dependencies import (
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
app.include_router(identity_context_router)
