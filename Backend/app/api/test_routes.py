from fastapi import APIRouter, Depends

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db


router = APIRouter(
    prefix="/test",
    tags=["Test"]
)


@router.get("/database")
def test_database(
    db: Session = Depends(get_db)
):

    result = db.execute(
        text("SELECT 1")
    )

    return {
        "database": "connected",
        "result": result.scalar()
    }