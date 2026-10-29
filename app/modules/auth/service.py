from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import DUMMY_HASH, create_access_token, verify_password
from app.modules.auth import repository as repo
from app.modules.auth.schemas import LoginRequest, TokenOut


def login(db: Session, data: LoginRequest) -> TokenOut:
    user = repo.get_user_by_email(db, data.school_id, data.email)
    # Same work and same error whether the email exists or the password is wrong.
    password_ok = verify_password(data.password, user.password_hash if user else DUMMY_HASH)
    if user is None or not password_ok:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        {
            "sub": str(user.id),
            "school_id": user.school_id,
            "role": user.role,
            "profile_id": user.teacher_id if user.role == "teacher" else user.parent_id,
        }
    )
    return TokenOut(access_token=token)
