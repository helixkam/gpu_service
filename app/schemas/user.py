from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    
    full_name: str | None = None
    email: EmailStr
    password: str
    
    
class UserOut(BaseModel):
    
    id: int
    email: EmailStr
    full_name: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True
        