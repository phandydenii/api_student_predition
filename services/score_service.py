from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

import schemas
from ml import ml_model
from models.student import Student
from models.subject import Subject
from schemas.score_schema import ScoreCreate
from models.score import Score
from utils.response import not_found, internal_error, success, success_new


# def get_scores_student(db: Session, student_id: int,year: int):
#     try:
#         data = db.query(Score).options(joinedload(Score.subject_id)).filter(Score.student_id == student_id,Score.year == year).all()
#         if data is None:
#             return not_found("Not found")
#         return data
#     except Exception as e:
#         db.rollback()
#         return internal_error(message=str(e))
#     finally:
#         db.commit()
#         db.close()

def get_scores_by_student(db: Session, student_id: int, year: int):
    try:
        data = (
            db.query(Score)
            .options(joinedload(Score.subject))
            .filter(Score.student_id == student_id, Score.year == year)
            .all()
        )
        count = 0
        total = 0
        for score in data:
            total += score.total
            count += 1
        total_average = total / count
        if not data:
            return not_found("Not found")
        return success_new(data,total_average, message="Success")
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.close()


def get_scores_by_grade_class(db: Session, grade_id: int, typeclass_id: int, year: int):
    try:
        # Get all students
        students = (
            db.query(Student)
            .filter(Student.grade_id == grade_id,
                    Student.typeclass_id == typeclass_id)
            .all()
        )

        if not students:
            raise HTTPException(status_code=404, detail="No students found")

        results = []

        for student in students:

            # Join subject
            sc_query = (
                db.query(Score)
                .options(joinedload(Score.subject))  # <-- LOAD subject object
                .filter(Score.student_id == student.id)
            )

            if year:
                sc_query = sc_query.filter(Score.year == year)

            scores = sc_query.all()

            student_scores = [
                {
                    "subject_id": s.subject_id,
                    "subject_name": s.subject.name if s.subject else None,
                    "year": s.year,
                    "month": s.month,
                    "homework": s.homework,
                    "monthly": s.monthly,
                    "social": s.social,
                    "absence": s.absence,
                    "total": s.total,

                    # 📌 Full Subject Object Here
                    "subject": {
                        "id": s.subject.id,
                        "name": s.subject.name,
                    } if s.subject else None
                }
                for s in scores
            ]

            results.append({
                "student_id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "scores": student_scores
            })

        return success(results, message="Success")

    except Exception as e:
        db.rollback()
        return internal_error(str(e))

    finally:
        db.close()


def create_score(db: Session, score_data: ScoreCreate):
    try:
        # Ensure student and subject exist (student check optional)
        subject = db.query(Subject).filter(Subject.id == score_data.subject_id).first()
        if not subject:
            raise not_found("Subject not found")

        # Calculate parts
        homework_part = score_data.homework * 0.2
        monthly_part = score_data.monthly * 0.7
        social_part = score_data.social * 0.1
        total_before_deduction = homework_part + monthly_part + social_part

        # Custom absence deduction per subject
        deduction_per_absence = subject.absence_deduction or 0.0
        absence_deduction_total = score_data.absence * deduction_per_absence

        total = total_before_deduction - absence_deduction_total
        if total < 0:
            total = 0.0

        # Map to letter grades and options
        # Using thresholds you described earlier:
        # A >= 45, B >=40, C >=35  => Option1 (good)
        # else D/E => Option2 (needs remedial)
        if total >= 45:
            letter = "A"
        elif total >= 40:
            letter = "B"
        elif total >= 35:
            letter = "C"
        elif total >= 30:
            letter = "D"
        else:
            letter = "E"

        option = "Option1" if letter in ("A", "B", "C") else "Option2"

        alert = None
        if score_data.absence >= 5:
            alert = f"Alert: Student absent {score_data.absence} times"

        db_score = Score(
            student_id=score_data.student_id,
            subject_id=score_data.subject_id,
            year=score_data.year,
            month=score_data.month,
            homework=score_data.homework,
            monthly=score_data.monthly,
            social=score_data.social,
            absence=score_data.absence,
            total=total,
            result_status=option
        )
        db.add(db_score)
        db.commit()
        db.refresh(db_score)

        ml_train_info = ml_model.train_model(db)
        data = {
            "score": db_score,
            "alert": alert,
            "ml_train": ml_train_info
        }
        return success(data,message="Success")
    except Exception as e:
        db.rollback()
        return internal_error(message=str(e))
    finally:
        db.commit()
        db.close()

def create_scores_batch(db: Session, scores_list: list[ScoreCreate]):
    results = []
    for s in scores_list:
        res = create_score(db, s)
        results.append(res)
    return results


