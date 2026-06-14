from sqlalchemy import (
    Column,
    BigInteger,
    DECIMAL,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey
)

from app.core.database import Base


class FraudFlag(Base):

    __tablename__ = "Fraud_Flag"

    Fraud_ID = Column(
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

    Risk_Score = Column(
        DECIMAL(5, 2)
    )

    Flag_Type = Column(
        String(100)
    )

    Description = Column(
        String(255)
    )

    Investigation_Status = Column(
        Enum(
            "Open",
            "Under_Review",
            "Resolved"
        ),
        default="Open"
    )

    Created_At = Column(
        TIMESTAMP
    )