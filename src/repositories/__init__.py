
"""
Repository package initialization.

This module exports all repository classes for easy importing.
Each repository provides database operations for its specific model.
"""
from src.repositories.user_repo import UserRepository
from src.repositories.job_repo import JobRepository
from src.repositories.quota_repo import QuotaRepository

__all__ = [
    'UserRepository',
    'JobRepository',   
    'QuotaRepository'  
]
