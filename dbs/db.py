from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
# pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic

DB_HOST = "localhost"
DB_NAME = "student_db"
DB_USER = "postgres"
# DB_PASSWORD = "123"
# DB_PORT = 5432

DB_PASSWORD = "root"
DB_PORT = 8080

URL_DATABASE = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
