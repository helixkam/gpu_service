from sqlalchemy import Column, Integer, ForeignKey
from src.models.base import base
from sqlalchemy import relationship

class Quota(base):
    """
    Quota model representing resource limits for each user.
    
    Attributes:
        id (int): Foreign key referencing the users table.
        user_id (int): Primary key - unique identifier for each quota.
        total_hours (int): Total GPU hours allocated to the user (default: 12).
        used_hours (int): GPU hours already consumed by the user (default: 0).
        user (relationship): One-to-one relationship with User model.
    """
    
    __tablename__ = "quota"
    
    id = Column(Integer, ForeignKey("users.id"))
    """Foreign key reference to the users table."""
    
    user_id = Column(Integer, primary_key=True)
    """Primary key - same as user id (one-to-one relationship)."""
    
    total_hours = Column(Integer, default=12)
    """Total allocated GPU hours."""
    
    used_hours = Column(Integer, default=0)
    """GPU hours consumed so far."""
    
    user = relationship('User', back_populates="quota")
    """User relationship - one-to-one (each quota belongs to one user)."""