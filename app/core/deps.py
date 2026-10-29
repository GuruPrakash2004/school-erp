from dataclasses import dataclass
from typing import Annotated, Literal

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db import get_db

DbSession = Annotated[Session, Depends(get_db)]

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class CurrentUser:
    id: int  # teachers.id or parents.id, depending on role
    school_id: int
    role: Literal["teacher", "parent"]


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> CurrentUser:
    if credentials is None:
        raise _unauthorized()
    try:
        claims = decode_access_token(credentials.credentials)
        role = claims["role"]
        if role not in ("teacher", "parent"):
            raise ValueError("bad role")
        return CurrentUser(
            id=int(claims["profile_id"]), school_id=int(claims["school_id"]), role=role
        )
    except (jwt.PyJWTError, KeyError, ValueError, TypeError):
        raise _unauthorized() from None


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
