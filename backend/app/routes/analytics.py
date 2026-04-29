from fastapi import APIRouter
from ..analytics_service import run_spark_analysis

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/run")
def run_analytics():
    return run_spark_analysis()