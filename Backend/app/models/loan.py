from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DECIMAL,
    Enum,
    Date,
    TIMESTAMP,
    ForeignKey,
    text
)

from app.core.database import Base


class Loan(Base):

    __tablename__ = "Loan"

    Loan_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Borrower_CIF = Column(
        BigInteger,
        ForeignKey("Customer.CIF_No"),
        nullable=False
    )

    Branch_ID = Column(
        Integer,
        ForeignKey("Branch.Branch_ID"),
        nullable=False
    )

    Loan_Type = Column(
        Enum(
            "Home",
            "Personal",
            "Education",
            "Vehicle",
            "Business"
        ),
        nullable=False
    )

    Loan_Status = Column(
        Enum(
            "Pending",
            "Active",
            "Closed",
            "Defaulted",
            "Rejected"
        ),
        default="Pending"
    )

    Principal_Amount = Column(
        DECIMAL(18, 2),
        nullable=False
    )

    Outstanding_Principal = Column(
        DECIMAL(18, 2),
        nullable=False
    )

    Interest_Rate = Column(
        DECIMAL(5, 2),
        nullable=False
    )

    Penalty_Rate = Column(
        DECIMAL(5, 2),
        default=2.00
    )

    Loan_Term_Months = Column(
        Integer,
        nullable=False
    )

    EMI_Amount = Column(
        DECIMAL(18, 2)
    )

    Total_Paid = Column(
        DECIMAL(18, 2),
        default=0
    )

    Start_Date = Column(Date)

    End_Date = Column(Date)

    Created_At = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )