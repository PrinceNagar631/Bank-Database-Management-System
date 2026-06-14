from sqlalchemy import (
    Column,
    BigInteger,
    Date,
    DECIMAL,
    ForeignKey
)

from app.core.database import Base


class DailyBalance(Base):

    __tablename__ = "Daily_Balance"

    Account_No = Column(
        BigInteger,
        ForeignKey("Account.Account_No"),
        primary_key=True,
        nullable=False
    )

    Balance_Date = Column(
        Date,
        primary_key=True,
        nullable=False
    )

    Closing_Balance = Column(
        DECIMAL(18, 2),
        nullable=False
    )