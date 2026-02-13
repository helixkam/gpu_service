from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.job import Job, JobStatus
from app.models.quota import Quota
from app.schemas.job import JobCreate

class JobServices:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def create(self, db: Session, job: JobCreate) -> Job:
        
        quota = self.db.query(Quota).filter(Quota.user_id == job.user_id).first()
        if (not quota) or (quota.is_active is False):
            raise HTTPException(
                status_code=403,
                detail="Quota not found or inactive!"
            )
            
        active_jobs = self.db.query(Job).filter(
            Job.user_id == job.user_id,
            Job.status.in_([JobStatus.QUEUED, Job.RUNNING])
        ).count()
        
        if not active_jobs >= quota.max_jobs:
            raise HTTPException(
                status_code=403, detail="Job Limit Exceeded."
            )
        
        
        db_job = Job(
            user_id=job.user_id,
            image=job.image,
            command=job.command,
            status=JobStatus.QUEUED,
            created_at=datetime.now()
        )
        
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        
        return db_job
    
    def list_jobs(self, db: Session) -> list[Job]:
        return self.db.query(Job).all()
    
    def get_job_by_id(self, db: Session, job_id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()    
            
        