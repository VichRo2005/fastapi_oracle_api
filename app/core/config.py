from pydantic import BaseSettings

class Settings(BaseSettings):
    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_HOST: str
    ORACLE_PORT: str
    ORACLE_SERVICE: str

    class Config:
        env_file = ".env"

settings = Settings()
