from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)


@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db)
):

    return (
        db.query(AuditLog)
        .order_by(
            AuditLog.Performed_At.desc()
        )
        .all()
    )