from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    get_current_user
)

from app.models.auth import LoginAuth

from app.schemas.otp import (
    GenerateOTPRequest,
    VerifyOTPRequest
)

from app.services.otp_service import (
    OTPService
)

router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)


@router.post("/generate")
def generate_otp(
    request: GenerateOTPRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return OTPService.generate_otp(
        db,
        current_user.User_ID,
        request.purpose
    )


@router.post("/verify")
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return OTPService.verify_otp(
        db,
        current_user.User_ID,
        request.otp,
        request.purpose
    )