from sqlalchemy import Column, Integer, String
from src.models.base import base
from sqlalchemy import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprected = "auto")
class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True,nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String,nullable=False)
    """Bcrypt hashed password - never stores plain text."""
    role = Column(String, default="user")
    """User role for authorization (default: 'user')."""

    jobs = relationship("Job",back_populates = "user",cascade = "all,delete")
    """One-to-many relationship: a user can have multiple jobs."""
    quota = relationship("Quota",back_populates = "user",uselist = False)
    """One-to-one relationship: each user has exactly one quota."""

    @staticmethod
    def hash_password(password:str) -> str :
        """
            Hash a plain text password using bcrypt.

            Args:
                password: Plain text password to hash
            
            Returns:
                Bcrypt hashed password string
            
            Raises:
                ValueError: If password is empty or None
        """
        if not password:
            raise ValueError("password can not be null")
        return pwd_context.hash(password)
       

    
    def verify_password(self,plain_password:str) -> bool:
        """
        Verify a plain text password against the stored hash.
        
        Args:
            plain_password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        if not plain_password or not self.hashed_password:
            return False
        return pwd_context.verify(plain_password,self.hashed_password)
        
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str, role: str= 'user'):
        hashed = cls.hash_password(password)
        return cls(username = username , email = email,hashed_password = hashed, role = role)
