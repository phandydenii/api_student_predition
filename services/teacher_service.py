from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.teacher import Teacher
from schemas.teacher_schema import TeacherBase
from utils.response import success, internal_error


def gets(db: Session) -> JSONResponse:
    try:
        students = db.query(Teacher).all()
        return success(students, "Successfully fetched")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()

def create(db: Session, data: TeacherBase)-> JSONResponse:
    try:
        db_student =Teacher(**data.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return success(db_student, f"Successfully created")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()