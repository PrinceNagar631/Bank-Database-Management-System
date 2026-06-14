from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.suspicious_activity_log import (
    SuspiciousActivityLog
)

router = APIRouter(
    prefix="/suspicious",
    tags=["Suspicious Activity"]
)


@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db)
):

    return (
        db.query(
            SuspiciousActivityLog
        )
        .order_by(
            SuspiciousActivityLog.Logged_At.desc()
        )
        .all()
    )