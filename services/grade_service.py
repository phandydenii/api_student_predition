from select import select

from sqlalchemy.orm import Session
from models.grade import Grade
from schemas.grade_schema import GradeRes, GradeReq
from utils.response import success, internal_error


def gets(db: Session):
    try:
        data = db.query(Grade).all()
        return success(data=data, message="Successfully fetched grades")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()



def get_grade(grade_id: int, db: Session):
    try:
        result = db.query(Grade).filter(Grade.id == grade_id).first()
        if not result:
            return success({}, "Grade not found")
        return success(result, "Successfully fetched")
    except Exception as e:
        return internal_error(str(e))
    finally:
        db.commit()
        db.close()

def create(db: Session, data: GradeReq)-> Grade:
    try:
        data =Grade(
            name=data.name,
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()