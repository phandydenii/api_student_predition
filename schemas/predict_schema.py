from pydantic import BaseModel


class PredictOut(BaseModel):
    predicted_option: str
    total_score: float