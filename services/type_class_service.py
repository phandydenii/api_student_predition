from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from models.type_class import TypeClass
from schemas.type_class_schema import TypeClassBase
from utils.response import success, internal_error, not_found


def gets(db: Session) -> JSONResponse:
    try:
        students = db.query(TypeClass).all()
        if len(students) == 0:
            return not_found("Data is empty")
        return success(students, "Successfully fetched students")
    except Exception as e:
        return internal_error(f"Failed to fetch students: {e}")
    finally:
        db.commit()
        db.close()

def get(type_class_id: int,db: Session) -> JSONResponse:
    try:
        data = db.query(TypeClass).filter(TypeClass.id == type_class_id).first()
        if data is None:
            return not_found("Data is empty")
        return success(data, "Successfully fetched students")
    except Exception as e:
        return internal_error(f"Failed to fetch students: {e}")
    finally:
        db.commit()
        db.close()

def create(data: TypeClassBase, db: Session) -> JSONResponse:
    try:
        db_student = TypeClass(**data.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return success(db_student)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
