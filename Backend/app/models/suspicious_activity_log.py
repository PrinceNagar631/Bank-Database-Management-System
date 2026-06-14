from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey
)

from app.core.database import Base


class SuspiciousActivityLog(Base):

    __tablename__ = "Suspicious_Activity_Log"

    Log_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Account_No = Column(
        BigInteger,
        ForeignKey(
            "Account.Account_No"
        )
    )

    Transaction_ID = Column(
        BigInteger,
        ForeignKey(
            "Transaction_Master.Transaction_ID"
        )
    )

    Activity_Type = Column(
        String(100)
    )

    Risk_Level = Column(
        Enum(
            "Low",
            "Medium",
            "High"
        )
    )

    Description = Column(
        String(255)
    )

    Logged_At = Column(
        TIMESTAMP
    )