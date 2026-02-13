from pydantic import BaseModel
from datetime import datetime


class QoutaOut(BaseModel):
    
    max_jobs: int
    max_gpu_hours: int
    used_gpu_hours: int
    gpu_types_allowed: list[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True