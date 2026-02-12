from typing import Optional, Protocol, TypedDict

class User(TypedDict):
    id: str
    email: str
    hashed_password: str
    role: str       # "user" یا "admin"
    is_active: bool

class UserRepo(Protocol):
    def get_by_email(self, email: str) -> Optional[User]: ...
    def get_by_id(self, user_id: str) -> Optional[User]: ...
