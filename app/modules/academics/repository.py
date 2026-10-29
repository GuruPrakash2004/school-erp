from decimal import Decimal

from sqlalchemy import Numeric, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db import Base


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int]
    class_id: Mapped[int]
    name: Mapped[str]


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int]
    name: Mapped[str]


class Mark(Base):
    __tablename__ = "marks"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int]
    student_id: Mapped[int]
    subject_id: Mapped[int]
    exam_name: Mapped[str]
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2))


class TeachingAssignment(Base):
    __tablename__ = "teaching_assignments"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int]
    teacher_id: Mapped[int]
    class_id: Mapped[int]
    subject_id: Mapped[int]


class StudentGuardian(Base):
    __tablename__ = "student_guardians"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int]
    student_id: Mapped[int]
    parent_id: Mapped[int]


def get_student(db: Session, school_id: int, student_id: int) -> Student | None:
    return db.scalars(
        select(Student).where(Student.school_id == school_id, Student.id == student_id)
    ).first()


def teacher_teaches_class(
    db: Session, school_id: int, teacher_id: int, class_id: int
) -> bool:
    return (
        db.scalars(
            select(TeachingAssignment.id).where(
                TeachingAssignment.school_id == school_id,
                TeachingAssignment.teacher_id == teacher_id,
                TeachingAssignment.class_id == class_id,
            )
        ).first()
        is not None
    )


def parent_is_guardian(
    db: Session, school_id: int, parent_id: int, student_id: int
) -> bool:
    return (
        db.scalars(
            select(StudentGuardian.id).where(
                StudentGuardian.school_id == school_id,
                StudentGuardian.parent_id == parent_id,
                StudentGuardian.student_id == student_id,
            )
        ).first()
        is not None
    )


def list_marks(db: Session, school_id: int, student_id: int) -> list[tuple[str, str, Decimal]]:
    rows = db.execute(
        select(Subject.name, Mark.exam_name, Mark.score)
        .join(Subject, (Subject.id == Mark.subject_id) & (Subject.school_id == Mark.school_id))
        .where(Mark.school_id == school_id, Mark.student_id == student_id)
        .order_by(Subject.name, Mark.exam_name)
    ).all()
    return [(r.name, r.exam_name, r.score) for r in rows]
