from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email,
        major=user.major,
        skills=user.skills,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()