# src/repositories/quota_repository.py
from sqlalchemy.orm import Session
from typing import Optional
from src.models.quota import Quota
from src.repositories.base_repo import BaseRepository

class QuotaRepository(BaseRepository[Quota]):
    """
    Repository for Quota model operations.
    
    This class handles all database operations related to user resource quotas,
    including quota creation, updates, and availability checks.
    Extends BaseRepository with Quota-specific methods.
    
    Attributes:
        db: SQLAlchemy database session inherited from BaseRepository
    """
    
    def __init__(self, db: Session):
        """
        Initialize the quota repository.
        
        Args:
            db: SQLAlchemy database session
        """
        super().__init__(db, Quota)
    
    def create(self, user_id: int, total_hours: int = 12) -> Quota:
        """
        Create a new quota for a user.
        
        This method is typically called when a new user is registered.
        
        Args:
            user_id: ID of the user
            total_hours: Total GPU hours allocated, defaults to 12
            
        Returns:
            Created Quota instance
        """
        quota = Quota(
            user_id=user_id,
            total_hours=total_hours,
            used_hours=0
        )
        self.db.add(quota)
        self.db.commit()
        self.db.refresh(quota)
        return quota
    
    def get_by_user(self, user_id: int) -> Optional[Quota]:
        """
        Retrieve quota for a specific user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Quota instance if found, None otherwise
        """
        return self.db.query(Quota).filter(Quota.user_id == user_id).first()
    
    def update_limits(self, user_id: int, total_hours: int = None, 
                     used_hours: int = None) -> Optional[Quota]:
        """
        Update quota limits for a user.
        
        Args:
            user_id: ID of the user
            total_hours: New total hours allocation (if None, keep current)
            used_hours: New used hours value (if None, keep current)
            
        Returns:
            Updated Quota instance if found, None otherwise
        """
        quota = self.get_by_user(user_id)
        if not quota:
            return None
        
        if total_hours is not None:
            quota.total_hours = total_hours
        if used_hours is not None:
            quota.used_hours = used_hours
        
        self.db.commit()
        self.db.refresh(quota)
        return quota
    
    def add_used_hours(self, user_id: int, hours: int) -> Optional[Quota]:
        """
        Add hours to the used quota.
        
        This method is called when a job is completed to track resource consumption.
        
        Args:
            user_id: ID of the user
            hours: Number of hours to add to used quota
            
        Returns:
            Updated Quota instance if found, None otherwise
        """
        quota = self.get_by_user(user_id)
        if not quota:
            return None
        
        quota.used_hours += hours
        self.db.commit()
        self.db.refresh(quota)
        return quota
    
    def reset_used_hours(self, user_id: int) -> Optional[Quota]:
        """
        Reset used hours to zero.
        
        This method is useful for monthly quota resets or plan upgrades.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Updated Quota instance if found, None otherwise
        """
        quota = self.get_by_user(user_id)
        if not quota:
            return None
        
        quota.used_hours = 0
        self.db.commit()
        self.db.refresh(quota)
        return quota
    
    def check_availability(self, user_id: int, required_hours: int) -> bool:
        """
        Check if user has sufficient quota hours for a job.
        
        Args:
            user_id: ID of the user
            required_hours: Hours required for the job
            
        Returns:
            True if remaining quota >= required hours, False otherwise
        """
        quota = self.get_by_user(user_id)
        if not quota:
            return False
        remaining = quota.total_hours - quota.used_hours
        return remaining >= required_hours
    
    def get_remaining_hours(self, user_id: int) -> Optional[int]:
        """
        Get remaining quota hours for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Remaining hours if quota exists, None otherwise
        """
        quota = self.get_by_user(user_id)
        if not quota:
            return None
        return quota.total_hours - quota.used_hours