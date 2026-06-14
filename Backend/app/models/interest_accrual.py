from sqlalchemy import (
    Column,
    BigInteger,
    Date,
    DateTime,
    DECIMAL,
    Enum,
    ForeignKey
)

from app.core.database import Base


class InterestAccrual(Base):

    __tablename__ = "Interest_Accrual"

    Accrual_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Account_No = Column(
        BigInteger,
        ForeignKey("Account.Account_No"),
        nullable=False
    )

    Accrual_Start_Date = Column(
        Date,
        nullable=False
    )

    Accrual_End_Date = Column(
        Date,
        nullable=False
    )

    Average_Balance = Column(
        DECIMAL(18, 2),
        nullable=False
    )

    Interest_Rate = Column(
        DECIMAL(5, 2),
        nullable=False
    )

    Interest_Amount = Column(
        DECIMAL(18, 2),
        nullable=False
    )

    Posted_Status = Column(
        Enum(
            "Pending",
            "Posted"
        ),
        default="Pending"
    )

    Posted_At = Column(
        DateTime
    )