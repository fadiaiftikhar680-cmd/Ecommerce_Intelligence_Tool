"""Authentication dependencies for protected catalog and event mutations."""

import hmac
import os

from fastapi import Header, HTTPException, status


def require_admin_api_key(
    api_key: str | None = Header(default=None, alias="X-Admin-API-Key")
) -> None:
    """Require the configured admin key for write/delete operations."""
    expected_key = os.getenv("ADMIN_API_KEY", "").strip()
    if not expected_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API is not configured. Set ADMIN_API_KEY on the backend.",
        )
    if not api_key or not hmac.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid X-Admin-API-Key header is required.",
        )
