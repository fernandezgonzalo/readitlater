from pydantic import BaseModel


class SiteIn(BaseModel):
    url: str


class SiteOut(BaseModel):
    url: str
    created: int
    readed: bool
    user_id: int