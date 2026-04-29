from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from ..celery_app import celery_app
from ..tasks import generate_matches_task

from .. import models
from ..database import get_db
from ..services import calculate_match_score

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/generate/{user_id}")
def generate_matches(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    jobs = db.query(models.Job).all()

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")

    db.query(models.Match).filter(models.Match.user_id == user_id).delete()

    created_matches = []

    for job in jobs:
        score, explanation = calculate_match_score(user, job)

        match = models.Match(
            user_id=user.id,
            job_id=job.id,
            score=score,
            explanation=explanation,
        )

        db.add(match)
        created_matches.append(match)

    db.commit()

    for match in created_matches:
        db.refresh(match)

    return created_matches


@router.get("/{user_id}")
def get_matches(user_id: int, db: Session = Depends(get_db)):
    matches = (
        db.query(models.Match)
        .filter(models.Match.user_id == user_id)
        .order_by(models.Match.score.desc())
        .all()
    )

    return matches

@router.post("/generate-async/{user_id}")
def generate_matches_async(user_id: int):
    task = generate_matches_task.delay(user_id)

    return {
        "message": "Matching task submitted",
        "task_id": task.id,
        "status": "queued",
    }


@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }