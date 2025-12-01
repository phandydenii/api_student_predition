import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
from sqlalchemy.orm import Session
import models
from fastapi import HTTPException
import os

from models.score import Score
from utils.response import internal_error

MODEL_PATH = "ml.student_model.pkl"

def train_model(db: Session):
    # load score rows with features + label
    rows = db.query(
        Score.homework,
        Score.monthly,
        Score.social,
        Score.absence,
        Score.result_status
    ).all()

    if not rows or len(rows) < 2:
        # need at least 1-2 rows; but warn user if not enough rows
        return {"message": "Not enough data to train model", "rows": len(rows)}

    df = pd.DataFrame(rows, columns=["homework", "monthly", "social", "absence", "result_status"])
    X = df[["homework", "monthly", "social", "absence"]]
    y = df["result_status"]  # Option1 / Option2

    model = DecisionTreeClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return {"message": "Model trained successfully", "trained_on": len(df)}

def predict(homework: float, monthly: float, social: float, absence: int):
    if not os.path.exists(MODEL_PATH):
        raise internal_error("Model not found. Train model first (/train/).")
    model = joblib.load(MODEL_PATH)
    total = homework * 0.2 + monthly * 0.7 + social * 0.1 - absence * 0.0  # absence deduction removed here: model predicts option as trained
    # prediction uses raw features
    pred = model.predict([[homework, monthly, social, absence]])[0]
    # Also compute a total using nothing about subject absence deduction -- it's subject-specific; keep returned total as raw calc
    total_calc = homework * 0.2 + monthly * 0.7 + social * 0.1 - absence * 0.0
    return {"predicted_option": pred, "total_score": total_calc}
