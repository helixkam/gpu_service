from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.quota import Quota
from app.schemas.user import UserCreate
from app.core.security import hash_passwd

class UserServices:
    def __init__(self, db: Session, ) -> None:
        self.db = db
    
    def create(self, user: UserCreate):
        existing = self.db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email Already Exists!"
            )
        db_user = User(
            email=user.email,
            hashed_password=hash_passwd(user.password),
            full_name=user.full_name
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        quota = Quota(user_id=db_user.id)
        self.db.add(quota)
        self.db.commit()
        
        return db_user
    
    def list_users(self, db: Session) -> list[User]:
        return self.db.query(User).all()
    
    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
        
