from .celery_app import celery_app
from .database import SessionLocal
from . import models
from .services import calculate_match_score


@celery_app.task(name="generate_matches_task")
def generate_matches_task(user_id: int):
    db = SessionLocal()

    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if not user:
            return {"status": "failed", "reason": "User not found"}

        jobs = db.query(models.Job).all()

        db.query(models.Match).filter(models.Match.user_id == user_id).delete()

        created = 0

        for job in jobs:
            score, explanation = calculate_match_score(user, job)

            match = models.Match(
                user_id=user.id,
                job_id=job.id,
                score=score,
                explanation=explanation,
            )

            db.add(match)
            created += 1

        db.commit()

        return {
            "status": "completed",
            "user_id": user_id,
            "matches_created": created,
        }

    finally:
        db.close()