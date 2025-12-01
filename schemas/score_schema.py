from typing import Optional

from pydantic import BaseModel


class ScoreBase(BaseModel):
    student_id: int
    subject_id: int
    year: int
    month: Optional[int] = None
    homework: float = 0.0
    monthly: float = 0.0
    social: float = 0.0
    absence: int = 0

class ScoreCreate(ScoreBase):
    pass

# For responses:
class ScoreOut(ScoreBase):
    id: int
    total: float
    result_status: Optional[str]