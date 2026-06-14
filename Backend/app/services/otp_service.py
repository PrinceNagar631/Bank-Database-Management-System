import random

from datetime import (
    datetime,
    timedelta
)

from fastapi import HTTPException

from app.models.otp import OTPStore
from app.models.auth import LoginAuth
from app.core.security import (
    hash_password,
    verify_password
)


class OTPService:

    @staticmethod
    def generate_otp(
        db,
        username,
        purpose
    ):

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        otp_record = OTPStore(

            User_ID=username,

            OTP_Hash=
            hash_password(otp),

            Purpose=purpose,

            Expires_At=
            datetime.utcnow()
            + timedelta(minutes=5),

            Is_Used=False
        )

        db.add(otp_record)

        db.commit()

        return {
            "message":
            "OTP generated",

            "otp":
            otp
        }

    @staticmethod
    def verify_otp(
        db,
        username,
        otp,
        purpose
    ):

        record = (

            db.query(OTPStore)

            .filter(
                OTPStore.User_ID
                == username,

                OTPStore.Purpose
                == purpose,

                OTPStore.Is_Used
                == False
            )

            .order_by(
                OTPStore.OTP_ID.desc()
            )

            .first()
        )

        if record is None:

            raise HTTPException(
                status_code=404,
                detail="OTP not found"
            )

        if datetime.utcnow() > record.Expires_At:

            raise HTTPException(
                status_code=400,
                detail="OTP expired"
            )

        if not verify_password(
            otp,
            record.OTP_Hash
        ):

            raise HTTPException(
                status_code=400,
                detail="Invalid OTP"
            )

        record.Is_Used = True

        user = (
            db.query(LoginAuth)
            .filter(
                LoginAuth.User_ID == username
            )
            .first()
        )

        user.OTP_Verified = True

        db.commit()

        return {
            "message":
            "OTP verified"
        }