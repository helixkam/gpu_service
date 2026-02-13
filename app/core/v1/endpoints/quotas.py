from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.qouta import QoutaOut
from app.services.quota_services import QuotaServices

router = APIRouter()

@router.get("/{user_id}", response_model=QoutaOut)
def get_quota(user_id: int, db: Session = Depends(get_db)):
    quota_services = QuotaServices(db)
    quota = quota_services.get_quota_by_user_id(db, user_id)
    if not quota:
        raise HTTPException(
            status_code=404, 
            detail="Quota not found!"
            )
    return quota
