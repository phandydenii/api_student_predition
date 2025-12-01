from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.subject import Subject
from schemas.subject_shema import SubjectBase
from utils.response import success, internal_error, not_found


def gets(db: Session) -> JSONResponse:
    try:
        students = db.query(Subject).all()
        if len(students) == 0:
            return not_found("Data not found")
        return success(students, "Successfully fetched")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()

def get(subject_id: int,db: Session) -> JSONResponse:
    try:
        data = db.query(Subject).filter(Subject.id == subject_id).first()
        if data is None:
            return not_found("Data not found")
        return success(data, "Successfully fetched")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()

def create(data: SubjectBase, db: Session)-> JSONResponse:
    try:
        db_student =Subject(**data.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return success(db_student, f"Successfully created")
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.close()