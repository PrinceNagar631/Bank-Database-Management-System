from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.fraud_flag import (
    FraudFlag
)

router = APIRouter(
    prefix="/fraud",
    tags=["Fraud"]
)


@router.get("/flags")
def get_flags(
    db: Session = Depends(get_db)
):

    return (
        db.query(FraudFlag)
        .order_by(
            FraudFlag.Created_At.desc()
        )
        .all()
    )