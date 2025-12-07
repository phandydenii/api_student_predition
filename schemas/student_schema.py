from datetime import date
from typing import Optional

from pydantic import BaseModel


class StudentBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender: str
    dob: date
    typeclass_id: int
    grade_id: int

class StudentSummary(BaseModel):
    student_id: int
    total_score: float
    average_score: float
    overall_status: str
    scores_count: int