from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from dbs.db import Base

class TypeClass(Base):
    __tablename__ = "typeclass"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)