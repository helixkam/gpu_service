from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.job import JobStatus

class JobCreate(BaseModel):
    
    user_id: int
    image: str
    command: str
    
class JobOut(BaseModel):
    
    id: int
    user_id: int
    image: str
    command: str
    status: JobStatus
    output: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    
    class Config:
        from_attributes = True