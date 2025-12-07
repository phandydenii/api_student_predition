from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dbs.db import get_db
from models.score import Score
from schemas.score_schema import ScoreCreate
from services import score_service
from utils.response import success, internal_error

router = APIRouter(prefix="/scores", tags=["Scores"])
@router.get("", response_class=JSONResponse, status_code=201)
def gets(student_id: int,year: int = 0,db: Session = Depends(get_db)):
    return score_service.get_scores_by_student(db,student_id,year)

@router.get("/filter", response_class=JSONResponse, status_code=201)
def gets(grade_id: int, typeclass_id: int,year: int = 0,db: Session = Depends(get_db)):
    return score_service.get_scores_by_grade_class(db,grade_id,typeclass_id,year)

@router.post("", response_class=JSONResponse, status_code=201)
def create(score_data: ScoreCreate,db: Session = Depends(get_db)):
    return score_service.create_score(db,score_data)

@router.post("/upload", response_class=JSONResponse, status_code=201)
async def upload_csv_pandas(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        df = df.fillna("")
        # Convert DataFrame to a list of dicts
        records = df.to_dict(orient="records")
        json = jsonable_encoder(records)
        print(json)
        required_columns = {"student_id", "subject_id","year", "month","homework","monthly","social","absence"}
        if not required_columns.issubset(df.columns):
            return internal_error(f"CSV must contain columns: {required_columns}")
        for row in json:
            data = ScoreCreate(
                student_id=row["student_id"],
                subject_id=row["subject_id"],
                year=row["year"],
                month=row["month"],
                homework=row["homework"],
                monthly=row["monthly"],
                social=row["social"],
                absence=row["absence"]
            )
            score_service.create_score(db,data)
        return success(None, f"Scores {len(records)} successfully uploaded csv file")
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()