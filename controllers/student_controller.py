from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dbs.db import get_db
from models.student import Student
from schemas.student_schema import StudentBase
from services import student_service
from utils.response import success,internal_error

router = APIRouter(prefix="/students", tags=["Student"])
@router.get("/all", response_class=JSONResponse, status_code=201)
def get_students(db: Session = Depends(get_db)):
    return student_service.get_students(db)

@router.get("/filter", response_class=JSONResponse, status_code=201)
def get_students(grade_id: int,class_type_id: int,db: Session = Depends(get_db)):
    return student_service.get_student_by_grade_class_type(grade_id,class_type_id, db)
@router.get("", response_class=JSONResponse, status_code=201)
def get_student(student_id: int,db: Session = Depends(get_db)):
    return student_service.get_student(student_id, db)
@router.post("", response_class=JSONResponse, status_code=201)
def create_student(req: StudentBase,db: Session = Depends(get_db)):
    return student_service.create_student(req, db)

@router.post("/batch", response_class=JSONResponse, status_code=201)
def create_students(req: list[StudentBase], db: Session = Depends(get_db)):
    return student_service.create_students(req, db)


@router.post("/update-load", response_class=JSONResponse, status_code=201)
async def upload_csv_pandas(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        # Convert DataFrame to a list of dicts
        data = df.to_dict(orient="records")
        json = jsonable_encoder(data)
        required_columns = {"first_name", "last_name", "gender","dob","grade_id","typeclass_id"}
        if not required_columns.issubset(df.columns):
            return internal_error(f"CSV must contain columns: {required_columns}")
        for row in json:
            student = StudentBase(
                first_name=row["first_name"],
                last_name=row["last_name"],
                gender=row["gender"],
                dob=row["dob"],
                grade_id=row["grade_id"],
                typeclass_id=row["typeclass_id"],
            )
            student_service.create_student(student, db)
        return success(None, f"Students {len(data)} successfully uploaded csv file")
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()