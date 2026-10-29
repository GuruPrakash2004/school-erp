from fastapi import APIRouter

from app.core.deps import CurrentUserDep, DbSession
from app.modules.academics import service
from app.modules.academics.schemas import StudentMarksOut

router = APIRouter(prefix="/students", tags=["academics"])


@router.get("/{student_id}/marks", response_model=StudentMarksOut)
def get_student_marks(student_id: int, db: DbSession, user: CurrentUserDep):
    return service.get_student_marks(db, user, student_id)
