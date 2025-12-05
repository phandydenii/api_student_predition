from collections import Counter

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import os, joblib
from ml import ml_model
from models.score import Score
from models.student import Student
from utils.response import internal_error


def student_summary(student_id: int,year: int, db: Session):
    scores = db.query(Score).filter(Score.student_id == student_id, Score.year == year).all()
    # scores = get_scores_student(db, student_id,year)
    # print(scores)
    if not scores:
        raise HTTPException(status_code=404, detail="No scores found for this student")
    total_score = sum(s.total for s in scores)
    average_score = total_score / len(scores) if scores else 0.0
    overall_status = "Option1" if average_score >= 35 else "Option2"
    data= {
        "student_id": student_id,
        "total_score": total_score,
        "average_score": average_score,
        "overall_status": overall_status,
        "scores_count": len(scores)
    }
    json_data = jsonable_encoder(data)
    return JSONResponse(
        content={
            "data": json_data,
            "status": {
                "code": "200",
                "message": "Success"
            }
        },
        status_code=200
    )


def predict_student_overall(student_id: int, db: Session):
    scores = db.query(Score).filter_by(student_id=student_id).all()
    if not scores:
        raise HTTPException(status_code=404, detail="No scores for this student")

    from collections import Counter

    if not os.path.exists(ml_model.MODEL_PATH):
        # If model not present, try to train automatically
        ml_model.train_model(db)
        if not os.path.exists(ml_model.MODEL_PATH):
            raise internal_error("Model not available. Train model first via /train/.")

    model = joblib.load(ml_model.MODEL_PATH)
    X = [[s.homework, s.monthly, s.social, s.absence] for s in scores]
    prediction = model.predict(X)
    overall_option = Counter(prediction).most_common(1)[0][0]
    total_score = sum(s.total for s in scores)
    average_score = total_score / len(scores)
    data = {
        "student_id": student_id,
        "overall_option": overall_option,
        "total_score": total_score,
        "average_score": average_score,
        "subject_predictions": list(prediction)
    }
    json_data = jsonable_encoder(data)
    return JSONResponse(
        content={
            "data": json_data,
            "status": {
                "code": "200",
                "message": "Success"
            }
        },
        status_code=200
    )

def predict_students_by_grade_class(grade_id: int, typeclass_id: int,year: int, db: Session):
    # Get all students matching grade and typeclass
    students = db.query(Student).filter(
        Student.grade_id == grade_id,
        Student.typeclass_id == typeclass_id
    ).all()

    if not students:
        raise HTTPException(status_code=404, detail="No students found for this grade and typeclass")

    # Load or train model
    if not os.path.exists(ml_model.MODEL_PATH):
        ml_model.train_model(db)
        if not os.path.exists(ml_model.MODEL_PATH):
            raise HTTPException(status_code=500, detail="Model not available. Train model first via /train/.")

    model = joblib.load(ml_model.MODEL_PATH)
    results = []

    for student in students:
        scores = db.query(Score).filter(Score.student_id ==student.id, Score.year == year).all()
        if not scores:
            continue  # skip students without scores

        X = [[s.homework, s.monthly, s.social, s.absence] for s in scores]
        prediction = model.predict(X)
        overall_option = Counter(prediction).most_common(1)[0][0]
        total_score = sum(s.total for s in scores)
        average_score = total_score / len(scores)

        results.append({
            "student_id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "overall_option": overall_option,
            "total_score": total_score,
            "average_score": average_score,
            "subject_predictions": list(prediction)
        })

    return JSONResponse(
        content={
            "data": jsonable_encoder(results),
            "status": {
                "code": "200",
                "message": f"Predictions fetched for {len(results)} students"
            }
        },
        status_code=200
    )