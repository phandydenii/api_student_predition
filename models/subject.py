from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from dbs.db import Base

class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    max_score = Column(Float, default=100.0)
    typeclass_id = Column(Integer, ForeignKey("typeclass.id"), nullable=True)
    absence_deduction = Column(Float, default=5.0)  # points to subtract per 1 absence for this subject
