from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str
    max_score: float
    typeclass_id: int
    absence_deduction: float = 5.0