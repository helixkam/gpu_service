from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_services import UserServices

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_services = UserServices(db)
    db_user = user_services.create(user)
    return db_user


@router.get("/", response_model=list[UserOut])
def list_of_users (db: Session = Depends(get_db)):
    user_services = UserServices(db)
    db_list = user_services.list_users(db)
    return db_list
    
    

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_services = UserServices(db)
    user = user_services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found!"
            )
    return user