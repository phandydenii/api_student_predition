from io import BytesIO
import pandas as pd
from fastapi import HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from starlette.responses import JSONResponse
from models.student import Student
from schemas.student_schema import StudentBase
from utils.response import success, internal_error, not_found


def get_students(db: Session) -> JSONResponse:
    try:
        students = (
            db.query(Student)
            .options(
                joinedload(Student.grade),
                joinedload(Student.typeclass)
            )
            .all()
        )

        # students = db.query(Student).all()
        if len(students) == 0:
            return not_found("Data not found")
        return success(students, "Successfully fetched students")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()

def get_student_by_grade_class_type(grade_id: int,class_type_id: int, db: Session):
    try:
        students = (
            db.query(Student)
            .options(
                joinedload(Student.grade),
                joinedload(Student.typeclass)
            )
            .filter(Student.grade_id == grade_id, Student.typeclass_id ==class_type_id)
            .all()
        )
        if not students:
            return not_found(message="Student not found")
        return success(students, "Successfully fetched student")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()

def get_student(student_id: int, db: Session):
    try:
        student = (
            db.query(Student)
            .options(
                joinedload(Student.grade),
                joinedload(Student.typeclass)
            )
            .filter(Student.id == student_id).first()
        )
        if not student:
            return not_found(message="Student not found")
        return success(student, "Successfully fetched student")
    except Exception as e:
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()


def create_student(data: StudentBase, db: Session) -> JSONResponse:
    try:
        db_student = Student(
            first_name=data.first_name,
            last_name=data.last_name,
            gender=data.gender,
            dob=data.dob,
            grade_id=data.grade_id,
            typeclass_id=data.typeclass_id
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return success(db_student)
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()


async def create_students(students: list[StudentBase], db: Session):
    try:
        if len(students) == 0:
            return not_found("Data not found")
        for student in students:
            student.id = student.id
            student.first_name = student.first_name
            student.last_name = student.last_name
            student.gender = student.gender
            student.dob = student.dob
            student.grade_id = student.grade_id
            student.typeclass_id = student.typeclass_id
            db.add(student)
            db.commit()
            db.refresh(student)
        return success(students, "Successfully created students")
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()


async def upload_csv_score(file: UploadFile = File(...), db: Session = None):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))
    # Convert DataFrame to a list of dicts
    data = df.to_dict(orient="records")
    json = jsonable_encoder(data)
    for dd in json:
        print(dd["homework"])
    return success(json)
    # try:
    #     if not file.filename.endswith(".csv"):
    #         return {"error": "File must be a CSV"}
    #
    #     # Read CSV into pandas DataFrame
    #     contents = await file.read()
    #     df = pd.read_csv(BytesIO(contents))
    #
    #     # Optional: check required columns
    #     required_columns = {"first_name", "last_name", "gender","dob","grade_id","typeclass_id"}
    #     if not required_columns.issubset(df.columns):
    #         return {"error": f"CSV must contain columns: {required_columns}"}
    #
    #     # Convert DataFrame to a list of dicts
    #     data = df.to_dict(orient="records")
    #     print(data)
    #     # Iterate rows and insert into DB
    #     for row in data:
    #         student = Student(
    #             first_name=row["first_name"],
    #             last_name=row["last_name"],
    #             gender=row["gender"],
    #             dob=row["dob"],
    #             grade_id=row["grade_id"],
    #             typeclass_id=row["typeclass_id"],
    #         )
    #         db.add(student)
    #
    #     db.commit()
    #     return success(None, f"{len(data)} students successfully uploaded")
    #
    # except Exception as e:
    #     db.rollback()
    #     return internal_error(message=str(e))