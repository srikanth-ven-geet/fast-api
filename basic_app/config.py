from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port:str = "5432"
    database_name: str = "fastapi"
    database_paswsord:str = "password123"
    database_username:str = "postgres"
    secret_key:str = "Welcome100"
    class Config:
        env_file="..env"

settings = Settings()
