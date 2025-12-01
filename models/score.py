from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from dbs.db import Base

class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    year = Column(Integer, nullable=True)  # 1-12
    month = Column(Integer, nullable=True)  # 1-12
    homework = Column(Float, default=0.0)
    monthly = Column(Float, default=0.0)
    social = Column(Float, default=0.0)
    absence = Column(Integer, default=0)
    total = Column(Float, default=0.0)
    result_status = Column(String(20), nullable=True)  # Option1 / Option2 or letter/option