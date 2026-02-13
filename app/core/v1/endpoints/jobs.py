from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.job import JobCreate, JobOut
from app.services.job_services import JobServices

router = APIRouter()

@router.post("/", response_model=JobOut)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    job_services = JobServices(db)
    db_job = job_services.create(db, job)
    return db_job

@router.get("/", response_model=list[JobOut])
def list_of_jobs(db: Session = Depends(get_db)):
    job_services = JobServices(db)
    db_list = job_services.list_jobs(db)
    return db_list

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job_services = JobServices(db)
    job = job_services.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(
            status_code=404, 
            detail="Job not found!"
            )
    return job
    