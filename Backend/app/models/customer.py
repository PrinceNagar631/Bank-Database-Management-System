from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Customer(Base):

    __tablename__ = "Customer"

    CIF_No = Column(
        BigInteger,
        primary_key=True
    )

    Customer_Type = Column(
        Enum(
            "Individual",
            "Organization"
        ),
        nullable=False
    )

    Email = Column(
        String(100),
        nullable=False,
        unique=True
    )

    Phone_No = Column(
        String(10),
        nullable=False,
        unique=True
    )

    # accounts = relationship(
    #     "AccountHolder",
    #     back_populates="customer"
    # )

    # login_auth = relationship(
    #     "LoginAuth",
    #     back_populates="customer",
    #     uselist=False
    # )

class IndividualCustomer(Base):

    __tablename__ = "Individual_Customer"

    CIF_No = Column(
        BigInteger,
        ForeignKey("Customer.CIF_No"),
        primary_key=True
    )

    Aadhaar = Column(
        String(12),
        unique=True,
        nullable=False
    )

    PAN = Column(
        String(10),
        unique=True,
        nullable=False
    )

    First_Name = Column(
        String(50),
        nullable=False
    )

    Last_Name = Column(
        String(50)
    )

    Gender = Column(
        String(20)
    )

    DOB = Column(
        Date
    )