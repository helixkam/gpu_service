from sqlalchemy.orm import Session
from app.models.quota import Quota

class QuotaServices:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def get_quota_by_user_id(self, db: Session, user_id: int) -> Quota | None:
        return self.db.query(Quota).filter(Quota.user_id == user_id).first()