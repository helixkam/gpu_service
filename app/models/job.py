from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Enum
)
from sqlalchemy.sql import func    
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.api.dependencies.db import Base

class JobStatus(PyEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(Base):
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    image = Column(String, nullable=False) 
    command = Column(String, nullable=False) 
    status = Column(
        Enum(JobStatus, name="status"),
        nullable=False,
        default=JobStatus.QUEUED
    )
    
    output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", back_populates="jobs")

