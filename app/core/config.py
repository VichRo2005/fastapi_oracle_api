from pydantic import BaseSettings

class Settings(BaseSettings):
    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_HOST: str
    ORACLE_PORT: str
    ORACLE_SERVICE: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
