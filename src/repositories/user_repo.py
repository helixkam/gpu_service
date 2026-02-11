# src/repositories/user_repository.py
from sqlalchemy.orm import Session
from typing import Optional, List
from src.models.user import User
from src.repositories.base_repo import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    This class handles all database operations related to users,
    including creation, authentication, and profile management.
    Extends BaseRepository with User-specific methods.
    Attributes:
        db: SQLAlchemy database session inherited from BaseRepository
    """
    
    def __init__(self, db: Session):
        """
        Initialize the user repository.
        Args:
            db: SQLAlchemy database session
        """
        super().__init__(db, User)
    
    def create(self, username: str, email: str, password: str, role: str = "user") -> User:
        """
        Create a new user with hashed password.
        
        This method automatically hashes the password using bcrypt
        before storing it in the database.
        
        Args:
            username: Unique username for the user
            email: Unique email address
            password: Plain text password (will be hashed)
            role: User role for authorization, defaults to "user"
            
        Returns:
            Created User instance with generated ID
            
        Raises:
            IntegrityError: If username or email already exists
        """
        user = User.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User instance if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        
        Args:
            username: Username to search for
            
        Returns:
            User instance if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Update user fields.
        
        Args:
            user_id: ID of the user to update
            **kwargs: Field-value pairs to update (e.g., role="admin", email="new@email.com")
            
        Returns:
            Updated User instance if found, None otherwise
            
        Note:
            Cannot update id or hashed_password through this method.
            Use update_password() for password changes.
        """
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key) and key not in ['id', 'hashed_password']:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """
        Update user's password.
        
        This method automatically hashes the new password before storing it.
        
        Args:
            user_id: ID of the user
            new_password: New plain text password
            
        Returns:
            True if password was updated, False if user not found
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        user.hashed_password = User.hash_password(new_password)
        self.db.commit()
        return True
    
    def verify_credentials(self, username_or_email: str, password: str) -> Optional[User]:
        """
        Verify user login credentials.
        
        This method checks both username and email fields and validates
        the password against the stored hash.
        
        Args:
            username_or_email: Either username or email
            password: Plain text password to verify
            
        Returns:
            User instance if credentials are valid, None otherwise
        """
        user = self.get_by_email(username_or_email) or self.get_by_username(username_or_email)
        if user and user.verify_password(password):
            return user
        return None