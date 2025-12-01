from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from controllers import (
    student_controller,
    grade_controller,
    ml_controller,
    score_controller,
    subject_controller,
    type_class_controller
)
from dbs.db import Base, engine
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Student API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
pre="/api/sms/v1"
app.include_router(student_controller.router, prefix=pre)
app.include_router(grade_controller.router, prefix=pre)
app.include_router(ml_controller.router, prefix=pre)
app.include_router(score_controller.router, prefix=pre)
app.include_router(subject_controller.router, prefix=pre)
app.include_router(type_class_controller.router, prefix=pre)

