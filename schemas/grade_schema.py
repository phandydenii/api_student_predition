from pydantic import BaseModel

class GradeReq(BaseModel):
    name: str

class GradeRes(BaseModel):
    id: int
    name: str

