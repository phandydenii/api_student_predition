from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from dbs.db import Base

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))