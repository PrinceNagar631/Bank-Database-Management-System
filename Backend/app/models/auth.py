from sqlalchemy import (
    Column,
    String,
    BigInteger,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class LoginAuth(Base):

    __tablename__ = "Login_Auth"

    User_ID = Column(
        String(50),
        primary_key=True
    )

    Customer_CIF = Column(
        BigInteger,
        ForeignKey("Customer.CIF_No"),
        unique=True
    )

    Password_Hash = Column(
        String(255),
        nullable=False
    )

    PIN_Hash = Column(
        String(255),
        nullable=False
    )

    OTP_Verified = Column(
        Boolean,
        default=False
    )

    # customer = relationship(
    #     "Customer",
    #     back_populates="login_auth"
    # )