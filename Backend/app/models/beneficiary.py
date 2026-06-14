from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    ForeignKey,
    TIMESTAMP
)

from app.core.database import Base


class Beneficiary(Base):

    __tablename__ = "Beneficiary"

    Beneficiary_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    Owner_CIF = Column(
        BigInteger,
        ForeignKey("Customer.CIF_No"),
        nullable=False
    )

    Nickname = Column(
        String(100)
    )

    Beneficiary_Name = Column(
        String(100),
        nullable=False
    )

    Beneficiary_Account_No = Column(
        BigInteger,
        nullable=False
    )

    Beneficiary_IFSC = Column(
        String(11),
        nullable=False
    )

    Beneficiary_Type = Column(
        Enum(
            "Internal",
            "External"
        ),
        default="Internal"
    )

    Status = Column(
        Enum(
            "Pending",
            "Active",
            "Blocked"
        ),
        default="Pending"
    )

    Added_At = Column(
        TIMESTAMP
    )