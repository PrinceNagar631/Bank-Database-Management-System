from fastapi import APIRouter
from fastapi import Depends

from app.core.security import (
    get_current_user
)

from app.models.auth import LoginAuth


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/me")
def get_me(
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return {
        "user_id": current_user.User_ID,
        "customer_cif": current_user.Customer_CIF
    }