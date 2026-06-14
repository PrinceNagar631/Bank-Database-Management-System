from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey
)

from sqlalchemy.sql import func

from app.core.database import Base


class LoginHistory(Base):

    __tablename__ = "Login_History"

    Login_History_ID = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    User_ID = Column(
        String(50),
        ForeignKey("Login_Auth.User_ID")
    )

    Login_Time = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )

    IP_Address = Column(
        String(50)
    )

    Device_Info = Column(
        String(255)
    )

    Login_Status = Column(
        Enum(
            "Success",
            "Failed"
        )
    )

    Failure_Reason = Column(
        String(255)
    )