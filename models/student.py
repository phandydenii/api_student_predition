from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from models.grade import Grade
from models.type_class import TypeClass
from dbs.db import Base

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10))
    dob = Column(Date, nullable=True)
    typeclass_id = Column(Integer, ForeignKey("typeclass.id"), nullable=True)
    grade_id = Column(Integer, ForeignKey("grade.id"), nullable=True)
