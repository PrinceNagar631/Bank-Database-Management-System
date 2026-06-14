from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Enum,
    Date,
    DateTime,
    DECIMAL,
    TIMESTAMP,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.models.branch import Branch
from app.core.database import Base


class Account(Base):
    # account_holders = relationship(
    #     "AccountHolder",
    #     back_populates="accounts",
    #     cascade="all, delete-orphan"
    # )

    # transactions = relationship(
    #     "TransactionEntry",
    #     back_populates="accounts"
    # )

    __tablename__ = "Account"

    Account_No = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Branch_ID = Column(
        Integer,
        ForeignKey("Branch.Branch_ID"),
        nullable=False
    )

    Account_Type = Column(
        Enum(
            "Savings",
            "Current"
        ),
        nullable=False
    )

    Account_Status = Column(
        Enum(
            "Pending",
            "Active",
            "Frozen",
            "Dormant",
            "Closed"
        ),
        default="Pending"
    )

    Currency_Code = Column(
        String(3),
        default="INR"
    )

    Current_Balance = Column(
        DECIMAL(18, 2),
        default=0.00
    )

    Available_Balance = Column(
        DECIMAL(18, 2),
        default=0.00
    )

    Open_Date = Column(
        Date,
        nullable=False
    )

    Close_Date = Column(
        Date
    )

    Last_Transaction_At = Column(
        DateTime
    )

    Created_At = Column(
        TIMESTAMP
    )


class SavingsAccount(Base):

    __tablename__ = "Savings_Account"

    Account_No = Column(
        BigInteger,
        ForeignKey("Account.Account_No"),
        primary_key=True
    )

    Interest_Rate = Column(
        DECIMAL(5,2),
        default=4.00
    )

    Minimum_Balance = Column(
        DECIMAL(18,2),
        default=1000.00
    )

    Withdrawal_Limit_Per_Day = Column(
        DECIMAL(18,2),
        default=50000.00
    )

class CurrentAccount(Base):

    __tablename__ = "Current_Account"

    Account_No = Column(
        BigInteger,
        ForeignKey("Account.Account_No"),
        primary_key=True
    )

    Overdraft_Limit = Column(
        DECIMAL(18,2),
        default=100000.00
    )

    Monthly_Charge = Column(
        DECIMAL(18,2),
        default=250.00
    )

    Minimum_Balance = Column(
        DECIMAL(18,2),
        default=10000.00
    )

class AccountHolder(Base):

    __tablename__ = "Account_Holder"

    Account_No = Column(
        BigInteger,
        ForeignKey("Account.Account_No"),
        primary_key=True
    )

    CIF_No = Column(
        BigInteger,
        ForeignKey("Customer.CIF_No"),
        primary_key=True
    )

    Holder_Type = Column(
        Enum(
            "Primary",
            "Secondary",
            "Guardian",
            "Authorized_Signatory"
        ),
        nullable=False
    )

    Ownership_Percentage = Column(
        DECIMAL(5,2),
        default=100.00
    )

    # account = relationship(
    #     "Account",
    #     back_populates="account_holders"
    # )

    # customer = relationship(
    #     "Customer",
    #     back_populates="accounts"
    # )