from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MIN: int = 60

settings = Settings()
