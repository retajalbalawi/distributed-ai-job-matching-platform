from fastapi import FastAPI

from .database import engine
from . import models
from .routes import users, jobs, matches
from .routes import analytics

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Distributed AI Job Matching Platform API",
    description="Backend API for profiles, jobs, matching, and analytics.",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(matches.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}