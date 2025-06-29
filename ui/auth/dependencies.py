from fastapi import Depends, HTTPException, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from .auth import decode_access_token
from .schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    cookie_token: Optional[str] = Cookie(None, alias="access_token")
):
    """Get the current user from the request."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Prefer header
    if not token and cookie_token:
        token = cookie_token
    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return User(username=username)