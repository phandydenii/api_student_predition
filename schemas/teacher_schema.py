from pydantic import BaseModel


class TeacherBase(BaseModel):
    first_name: str
    last_name: str