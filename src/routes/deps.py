from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.repository.user_repo import UserRepo
from src.utils.security import read_token
from src.routes.auth import get_user_repo  # همون DI

bearer = HTTPBearer(auto_error=False)

def current_user(
    cred: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
    repo: UserRepo = Depends(get_user_repo),
):
    if not cred:
        raise HTTPException(401, "Not logged in")

    try:
        payload = read_token(cred.credentials)
    except ValueError:
        raise HTTPException(401, "Bad token")

    u = repo.get_by_id(payload["sub"])
    if not u or not u["is_active"]:
        raise HTTPException(401, "User not found/disabled")

    return u

def admin_only(u=Depends(current_user)):
    if u["role"] != "admin":
        raise HTTPException(403, "Admin only")
    return u
