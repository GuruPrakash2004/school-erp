from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int]
    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
    teacher_id: Mapped[int | None]
    parent_id: Mapped[int | None]


def get_user_by_email(db: Session, school_id: int, email: str) -> User | None:
    return db.scalars(
        select(User).where(User.school_id == school_id, User.email == email)
    ).first()
