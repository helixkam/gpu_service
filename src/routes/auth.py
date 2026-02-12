from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.repository.user_repo import UserRepo
from src.utils.security import make_token, verify_pw

router = APIRouter(prefix="/auth", tags=["auth"])

# دوستانت اینو با DI واقعی وصل کنن
def get_user_repo() -> UserRepo:
    raise NotImplementedError

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(data: LoginIn, repo: UserRepo = Depends(get_user_repo)):
    u = repo.get_by_email(str(data.email))
    if not u or not u["is_active"]:
        raise HTTPException(401, "Invalid credentials")

    if not verify_pw(data.password, u["hashed_password"]):
        raise HTTPException(401, "Invalid credentials")

    return {"access_token": make_token(u["id"], u["role"]), "token_type": "bearer"}
