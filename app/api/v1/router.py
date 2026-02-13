from fastapi import APIRouter
from .endpoints import users, jobs, quotas

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(quotas.router, prefix="/quotas", tags=["Quotas"])