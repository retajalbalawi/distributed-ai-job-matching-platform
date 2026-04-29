from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/")
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    new_job = models.Job(
        title=job.title,
        company=job.company,
        location=job.location,
        required_skills=job.required_skills,
        description=job.description,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()
