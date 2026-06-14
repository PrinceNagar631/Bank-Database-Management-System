from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    get_current_user
)

from app.models.auth import (
    LoginAuth
)

from app.schemas.account import (
    CreateSavingsAccountRequest,
    CreateCurrentAccountRequest
)

from app.services.account_service import (
    AccountService
)


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/create-savings")
def create_savings_account(
    request: CreateSavingsAccountRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        AccountService
        .create_savings_account(
            db,
            request.branch_id,
            current_user.Customer_CIF
        )
    )


@router.post("/create-current")
def create_current_account(
    request: CreateCurrentAccountRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        AccountService
        .create_current_account(
            db,
            request.branch_id,
            current_user.Customer_CIF
        )
    )

@router.get("/my-accounts")
def get_my_accounts(
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        AccountService
        .get_my_accounts(
            db,
            current_user.Customer_CIF
        )
    )