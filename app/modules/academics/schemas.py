from pydantic import BaseModel


class MarkOut(BaseModel):
    subject: str
    exam_name: str
    score: float


class StudentMarksOut(BaseModel):
    student_id: int
    student_name: str
    marks: list[MarkOut]
