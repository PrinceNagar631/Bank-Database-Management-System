from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    DateTime,
    Boolean,
    ForeignKey,
    TIMESTAMP
)

from app.core.database import Base


class OTPStore(Base):

    __tablename__ = "OTP_Store"

    OTP_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    User_ID = Column(
        String(50),
        ForeignKey("Login_Auth.User_ID"),
        nullable=False
    )

    OTP_Hash = Column(
        String(255),
        nullable=False
    )

    Purpose = Column(
        Enum(
            "Login",
            "Transaction",
            "Password_Reset"
        ),
        nullable=False
    )

    Generated_At = Column(
        TIMESTAMP
    )

    Expires_At = Column(
        DateTime,
        nullable=False
    )

    Is_Used = Column(
        Boolean,
        default=False
    )