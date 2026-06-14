from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum
)

from app.core.database import Base


class Branch(Base):

    __tablename__ = "Branch"

    Branch_ID = Column(
        Integer,
        primary_key=True
    )

    Branch_Name = Column(
        String(100)
    )

    IFSC_Code = Column(
        String(11)
    )

    Branch_Status = Column(
        Enum(
            "Active",
            "Inactive"
        )
    )