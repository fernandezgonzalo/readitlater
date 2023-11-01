from typing import List, Annotated

from fastapi import APIRouter, Depends

from api.dependencies import get_session
from sqlmodel import Session, select
from api.models import Users
from .schemas import UserIn, UserOut
from api.routers.auth.schemas import User
from api.routers.auth.utils import get_current_active_user

from .utils import verify_password, get_password_hash


router = APIRouter()


@router.get("/users", response_model=List[UserOut])
def get_users(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    statement = select(Users)
    results = session.exec(statement).all()

    return results


@router.post("/users")
def create_user(
    *,
    session: Session = Depends(get_session),
    user: UserIn
):
    password_hashed = get_password_hash(user.password)
    user = Users(
        username=user.username,
        password_hash=password_hashed
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return True
