from fastapi import FastAPI
from app.api.v1.router import api_router
from app.api.dependencies import init_database

gpuaas_app = FastAPI()

init_database()

gpuaas_app.include_router(api_router)
