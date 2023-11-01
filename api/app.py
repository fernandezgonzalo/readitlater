from fastapi import FastAPI
from .models import create_db_and_tables, engine, Users, Sites
from .dependencies import get_session

from .routers.sites import sites
from .routers.users import users
from .routers.auth import auth


app = FastAPI()
app.include_router(
    sites.router,
    prefix="/sites",
    tags=["Sites"],
    # dependencies=[Depends(get_token_header)]
)
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)


@app.on_event("startup")
def on_starup():
    create_db_and_tables()


@app.get("/")
async def health():
    return {"status": "OK"}


# session: Session = Depends(get_session)