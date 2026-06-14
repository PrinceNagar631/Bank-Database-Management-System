from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.schemas.loan_schema import LoanApplyRequest
from app.services.loan_service import LoanService

router = APIRouter(
    prefix="/loan",
    tags=["Loan"]
)


@router.post("/apply")
def apply_loan(
    request: LoanApplyRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return LoanService.apply(
        db,
        current_user.Customer_CIF,
        request
    )


@router.get("/my-loans")
def my_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return LoanService.get_my_loans(
        db,
        current_user.Customer_CIF
    )

@router.post("/approve/{loan_id}")
def approve_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    return LoanService.approve_loan(
        db,
        loan_id
    )


@router.post("/reject/{loan_id}")
def reject_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    return LoanService.reject_loan(
        db,
        loan_id
    )