from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dbs.db import get_db
from schemas.subject_shema import SubjectBase
from services import subject_service
from utils.response import success, internal_error

router = APIRouter(prefix="/subjects", tags=["Subjects"])
@router.get("", response_class=JSONResponse, status_code=201)
def gets(db: Session = Depends(get_db)):
    return subject_service.gets(db)
@router.get("/{subject_id}", response_class=JSONResponse, status_code=201)
def get(subject_id: int,db: Session = Depends(get_db)):
    return subject_service.get(subject_id,db)
@router.post("", response_class=JSONResponse, status_code=201)
def create(req: SubjectBase,db: Session = Depends(get_db)):
    return subject_service.create(req, db)