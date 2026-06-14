from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    Enum,
    ForeignKey,
    TIMESTAMP
)

from app.core.database import Base


class LoginSession(Base):

    __tablename__ = "Login_Session"

    Session_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    User_ID = Column(
        String(50),
        ForeignKey("Login_Auth.User_ID")
    )

    JWT_ID = Column(
        String(255),
        unique=True,
        nullable=False
    )

    IP_Address = Column(
        String(50)
    )

    Device_Info = Column(
        String(255)
    )

    Login_Time = Column(
        TIMESTAMP
    )

    Expiry_Time = Column(
        DateTime,
        nullable=False
    )

    Logout_Time = Column(
        DateTime
    )

    Session_Status = Column(
        Enum(
            "Active",
            "Expired",
            "Logged_Out",
            "Revoked"
        ),
        default="Active"
    )