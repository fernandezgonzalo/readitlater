from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine
from api.settings import settings

# pasar a minuscula los modelos
class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: bytes
    created: int = Field(default=datetime.utcnow().timestamp())
    disabled: bool = Field(default=False)



class Sites(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    created: int = Field(default=datetime.utcnow().timestamp())
    readed: bool = Field(default=False)

    user_id: int = Field(default=None, foreign_key="users.id")


# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
database_url = settings.DATABASE_URL

engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

