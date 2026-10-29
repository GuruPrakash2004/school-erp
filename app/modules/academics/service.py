from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser
from app.modules.academics import repository as repo
from app.modules.academics.schemas import MarkOut, StudentMarksOut


def can_view_student(db: Session, user: CurrentUser, student: repo.Student) -> bool:
    if user.role == "teacher":
        return repo.teacher_teaches_class(db, user.school_id, user.id, student.class_id)
    if user.role == "parent":
        return repo.parent_is_guardian(db, user.school_id, user.id, student.id)
    return False


def get_student_marks(db: Session, user: CurrentUser, student_id: int) -> StudentMarksOut:
    student = repo.get_student(db, user.school_id, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if not can_view_student(db, user, student):
        raise HTTPException(status_code=403, detail="You are not allowed to view this student")

    marks = repo.list_marks(db, user.school_id, student.id)
    return StudentMarksOut(
        student_id=student.id,
        student_name=student.name,
        marks=[MarkOut(subject=s, exam_name=e, score=float(sc)) for s, e, sc in marks],
    )
