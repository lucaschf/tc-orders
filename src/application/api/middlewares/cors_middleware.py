from typing import Iterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI, allowed_origins: Iterable[str]) -> None:
    """Configure Cross-Origin Resource Sharing (CORS) for the FastAPI application.

    Args:
        app: The FastAPI application instance.
        allowed_origins: A list of allowed origins for CORS.

    Returns:
        None
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


__all__ = ["setup_cors"]
