from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.daily_balance import DailyBalance

router = APIRouter(
    prefix="/daily-balance",
    tags=["Daily Balance"]
)


@router.get("/{account_no}")
def get_daily_balance(
    account_no: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(DailyBalance)
        .filter(
            DailyBalance.Account_No == account_no
        )
        .all()
    )
    