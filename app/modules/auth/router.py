from fastapi import APIRouter

from app.core.deps import DbSession
from app.modules.auth import service
from app.modules.auth.schemas import LoginRequest, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest, db: DbSession):
    return service.login(db, data)
