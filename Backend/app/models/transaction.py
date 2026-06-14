from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    DateTime,
    DECIMAL,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class TransactionMaster(Base):

    __tablename__ = "Transaction_Master"

    Transaction_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Transaction_Type = Column(
        Enum(
            "Deposit",
            "Withdrawal",
            "Transfer",
            "Interest_Credit",
            "Charge_Debit",
            "Refund"
        )
    )

    Transaction_Status = Column(
        Enum(
            "Pending",
            "Success",
            "Failed",
            "Reversed"
        )
    )

    Initiated_By_User = Column(
        String(50),
        ForeignKey("Login_Auth.User_ID")
    )

    Reference_Number = Column(
        String(100),
        unique=True
    )

    Remarks = Column(
        String(255)
    )

    Created_At = Column(
        TIMESTAMP
    )

    Completed_At = Column(
        DateTime
    )

    # entries = relationship(
    #     "TransactionEntry",
    #     back_populates="transaction"
    # )


class TransactionEntry(Base):

    __tablename__ = "Transaction_Entry"

    Entry_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Transaction_ID = Column(
        BigInteger,
        ForeignKey(
            "Transaction_Master.Transaction_ID"
        )
    )

    Account_No = Column(
        BigInteger,
        ForeignKey("Account.Account_No")
    )

    Entry_Type = Column(
        Enum(
            "Debit",
            "Credit"
        )
    )

    Amount = Column(
        DECIMAL(18,2)
    )

    Balance_After = Column(
        DECIMAL(18,2)
    )

    Entry_Time = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )

    # account = relationship(
    #     "Account",
    #     back_populates="transactions"
    # )

    # transaction = relationship(
    #     "TransactionMaster",
    #     back_populates="entries"
    # )