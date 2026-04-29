from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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