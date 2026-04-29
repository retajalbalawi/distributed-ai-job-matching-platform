from fastapi import FastAPI

app = FastAPI(
    title="Distributed AI Job Matching Platform API",
    description="Backend API for profile management, job listings, matching, and analytics.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Distributed AI Job Matching Platform API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }