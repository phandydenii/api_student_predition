from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dbs.db import get_db
from schemas.grade_schema import GradeReq
from services import grade_service

router = APIRouter(prefix="/grades", tags=["Grades"])
@router.get("/all", response_class=JSONResponse)
def get_students(db: Session = Depends(get_db)):
    return grade_service.gets(db)

@router.get("", response_class=JSONResponse)
def get_students(grade_id: int, db: Session = Depends(get_db)):
    return grade_service.get_grade(grade_id, db)
@router.post("", response_class=JSONResponse, status_code=201)
def create_student(req: GradeReq,db: Session = Depends(get_db)):
    return grade_service.create(db,req)