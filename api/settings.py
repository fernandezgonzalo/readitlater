from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "b5abe683e8a5dbf65d0ad8b42d7d029bd9216049b57b6aa84948c05ff2eb8802"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL = "sqlite:///database.db"


settings = Settings()