from fastapi import (
    APIRouter,
    Depends,
    Request
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session
from app.core.security import oauth2_scheme
from app.services.auth_service import AuthService

from app.core.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    return AuthService.login(
        db,
        form_data.username,
        form_data.password,
        request
    )

@router.post("/logout")
def logout(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(
        get_db
    )
):

    return AuthService.logout(
        db,
        token
    )