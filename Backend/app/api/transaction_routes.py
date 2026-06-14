from fastapi import (
    APIRouter,
    Depends,
    Query
)
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    get_current_user
)
from app.models.auth import LoginAuth
from app.schemas.transaction import (
    DepositRequest,
    WithdrawRequest,
    TransferRequest
)
from app.services.transaction_service import (
    TransactionService
)
from datetime import datetime

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/deposit")
def deposit(
    request: DepositRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        TransactionService.deposit(
            db,
            request.account_no,
            request.amount,
            current_user.User_ID,
            current_user.Customer_CIF
        )
    )

@router.post("/withdraw")
def withdraw(
    request: WithdrawRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        TransactionService.withdraw(
            db,
            request.account_no,
            request.amount,
            current_user.User_ID,
            current_user.Customer_CIF
        )
    )

@router.post("/transfer")
def transfer(
    request: TransferRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        TransactionService.transfer(
            db,
            request.from_account,
            request.to_account,
            request.amount,
            current_user.User_ID,
            current_user.Customer_CIF
        )
    )

@router.get(
    "/history/{account_no}"
)
def transaction_history(
    account_no: int,
    db: Session = Depends(
        get_db
    ),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        TransactionService
        .get_transaction_history(
            db,
            account_no,
            current_user.Customer_CIF
        )
    )

@router.get(
    "/mini-statement/{account_no}"
)
def mini_statement(
    account_no: int,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        TransactionService
        .get_mini_statement(
            db,
            account_no,
            current_user.Customer_CIF
        )
    )

@router.get(
    "/account-statement"
)
def account_statement(
    account_no: int,
    from_date: str,
    to_date: str,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        TransactionService
        .get_account_statement(
            db,
            account_no,
            datetime.strptime(
                from_date,
                "%Y-%m-%d"
            ),
            datetime.strptime(
                to_date,
                "%Y-%m-%d"
            ),
            current_user.Customer_CIF
        )
    )