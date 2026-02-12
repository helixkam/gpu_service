from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.sql import func    
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import JSON

from app.api.dependencies.db import Base


class Quota(Base):
    
    __tablename__ = "quotas"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    max_jobs = Column(Integer, default=13)
    max_gpu_hours = Column(Integer, default=12)
    used_gpu_hours = Column(Integer, default=0)
    gpu_types_allowed = Column(JSON, default=["V100", "A100"])
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="quota")