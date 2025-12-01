from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dbs.db import get_db
from services import ml_service
from services.ml_service import student_summary, predict_student_overall, predict_students_by_grade_class
from utils.response import success, internal_error

router = APIRouter(prefix="/machine-learning", tags=["Machine-Learning"])
@router.get("/summary/{student_id}", response_class=JSONResponse, status_code=201)
def summary_student(student_id: int,db: Session = Depends(get_db)):
    return student_summary(student_id, db)

@router.post("/predict/{student_id}", response_class=JSONResponse, status_code=201)
def create_student(student_id: int,db: Session = Depends(get_db)):
    return predict_student_overall(student_id,db)

@router.post("/predict-by-filter", response_class=JSONResponse, status_code=201)
def create_student(grade_id: int, typeclass_id: int,db: Session = Depends(get_db)):
    return predict_students_by_grade_class(grade_id,typeclass_id,db)