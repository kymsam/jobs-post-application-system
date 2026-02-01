import redis
import json
from sqlalchemy.orm import Session
from ..config import settings
from ..Database import get_db
from .. import models
from .cache import redis_client


def fetch_job_from_db(job_id: int, db: Session):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        return None
    print("Fetching Job from the database ▦")
    return {"id": job.id, "title": job.Job_position, "description": job.Job_description}

def search_jobs(job_id: int, db: Session):
    cache_key = f"job_search:{job_id}"

    # Check cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        print("Returning cached result...")
        return json.loads(cached_result)

    # Otherwise fetch from DB
    job = fetch_job_from_db(job_id, db)
    if not job:
        return None

    # Store in cache with TTL (e.g., 60 seconds)
    redis_client.setex(cache_key, 60, json.dumps(job))

    return job
