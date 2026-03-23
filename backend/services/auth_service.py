import os
from functools import lru_cache
from typing import Any, Dict

import requests
from jose import ExpiredSignatureError, JWTError, jwt


SUPABASE_URL = os.getenv("SUPABASE_URL")


class JWKSFetchError(Exception):
    """Raised when Supabase JWKS cannot be fetched or parsed."""


@lru_cache(maxsize=1)
def _get_supabase_jwks() -> Dict[str, Any]:
    if not SUPABASE_URL:
        raise JWKSFetchError("SUPABASE_URL is not configured")

    jwks_url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"

    try:
        response = requests.get(jwks_url, timeout=5)
        response.raise_for_status()
        jwks = response.json()
    except requests.RequestException as exc:
        raise JWKSFetchError(f"Failed to fetch JWKS: {exc}") from exc
    except ValueError as exc:
        raise JWKSFetchError("Invalid JWKS JSON response") from exc

    keys = jwks.get("keys") if isinstance(jwks, dict) else None
    if not isinstance(keys, list) or not keys:
        raise JWKSFetchError("JWKS payload does not contain keys")

    return jwks


def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    """Verify a Supabase access token using its JWKS key set (ES256)."""
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise JWTError("Invalid token header") from exc

    kid = header.get("kid")
    if not kid:
        raise JWTError("Token header missing kid")

    jwks = _get_supabase_jwks()
    key = next((k for k in jwks["keys"] if k.get("kid") == kid), None)
    if not key:
        # Refresh once in case keys rotated since cache fill.
        _get_supabase_jwks.cache_clear()
        jwks = _get_supabase_jwks()
        key = next((k for k in jwks["keys"] if k.get("kid") == kid), None)

    if not key:
        raise JWTError("No matching JWKS key found for token kid")

    try:
        return jwt.decode(token, key, algorithms=["ES256"], options={"verify_aud": False})
    except ExpiredSignatureError:
        raise
    except JWTError:
        raise
