from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from dbs.db import get_db
from schemas.type_class_schema import TypeClassBase
from services import type_class_service
from utils.response import success, internal_error

router = APIRouter(prefix="/type-class", tags=["Type classes"])
@router.get("/all")
def gets(db: Session = Depends(get_db))->JSONResponse:
    return type_class_service.gets(db)
@router.get("")
def gets(type_class_id: int,db: Session = Depends(get_db))->JSONResponse:
    return type_class_service.get(type_class_id,db)
@router.post("", response_class=JSONResponse, status_code=201)
def create(req: TypeClassBase,db: Session = Depends(get_db)):
    return type_class_service.create(req, db)