from typing import List

from fastapi import APIRouter

job_router = APIRouter()

@job_router.get("/")
async def get_all_job_router() -> List[dict]:
    job = [
        {"id": 10, "name": "Kwafo Samuel", "cleaning_type": "full_clean", "price_per_hour": 29.99},
        {"id": 12, "name": "Festus Ofori", "cleaning_type": "spot_clean", "price_per_hour": 19.99}
    ]
    return job