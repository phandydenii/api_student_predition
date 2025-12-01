from sqlalchemy import Column, Integer, String
from dbs.db import Base

class Grade(Base):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)