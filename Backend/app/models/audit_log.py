from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    JSON,
    TIMESTAMP
)
from sqlalchemy.sql import func

from app.core.database import Base


class AuditLog(Base):

    __tablename__ = "Audit_Log"

    Audit_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Table_Name = Column(
        String(100),
        nullable=False
    )

    Operation_Type = Column(
        Enum(
            "INSERT",
            "UPDATE",
            "DELETE"
        ),
        nullable=False
    )

    Record_Primary_Key = Column(
        String(255)
    )

    Performed_By = Column(
        String(50)
    )

    Old_Value = Column(
        JSON
    )

    New_Value = Column(
        JSON
    )

    Performed_At = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )