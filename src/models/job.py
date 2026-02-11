from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import relationship 
from src.models.base import base 

class Job(base):
    """
    Job model representing computing tasks submitted by users.
    
    Attributes:
        id (int): Primary key - unique identifier for each job.
        user_id (int): Foreign key referencing the users table.
        gpu_count (int): Number of GPU units required for this job.
        est_hours (int): Estimated execution time in hours.
        command (str): The actual command/script to be executed.
        status (str): Current job status (PENDING, RUNNING, COMPLETED, FAILED, etc.).
        user (relationship): Many-to-one relationship with User model.
    """
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    """Unique job identifier."""
    
    user_id = Column(Integer, ForeignKey("users.id"))
    """Foreign key reference to the user who submitted this job."""
    
    gpu_count = Column(Integer, nullable=False)
    """Number of GPU units required."""
    
    est_hours = Column(Integer, nullable=False)
    """Estimated runtime in hours."""
    
    command = Column(String)
    """Execution command or script path."""
    
    status = Column(String, default="PENDING")
    """Current job status."""
    
    user = relationship("User", back_populates="jobs")
    """User relationship - many jobs belong to one user."""