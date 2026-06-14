from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.services.interest_accrual_service import (
    InterestAccrualService
)

router = APIRouter(
    prefix="/interest",
    tags=["Interest"]
)


@router.post("/calculate")
def calculate_interest(
    account_no: int,
    rate: float,
    db: Session = Depends(get_db)
):

    return InterestAccrualService.create_interest(
        db=db,
        account_no=account_no,
        start_date=date(
            2026,
            6,
            1
        ),
        end_date=date(
            2026,
            6,
            30
        ),
        annual_rate=rate
    )