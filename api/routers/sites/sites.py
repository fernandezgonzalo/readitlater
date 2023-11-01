from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from api.dependencies import get_session
from api.models import Sites
from .schemas import SiteIn, SiteOut
from typing import Annotated
from api.routers.auth.schemas import User
from api.routers.auth.utils import get_current_active_user


router = APIRouter()


@router.get("/sites")
def get_sites(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    statement = select(Sites).where(Sites.user_id == current_user.id)
    results = session.exec(statement).all()

    return results


@router.post("/sites", response_model=SiteOut)
def create_site(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)],
    site: SiteIn
):
    site = Sites(
        url=site.url,
        user_id=current_user.id
    )
    session.add(site)
    session.commit()
    session.refresh(site)

    return site