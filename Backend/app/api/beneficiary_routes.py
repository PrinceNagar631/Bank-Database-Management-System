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

from app.schemas.beneficiary import (
    AddBeneficiaryRequest
)

from app.services.beneficiary_service import (
    BeneficiaryService
)

router = APIRouter(
    prefix="/beneficiaries",
    tags=["Beneficiaries"]
)


@router.post("/add")
def add_beneficiary(
    request: AddBeneficiaryRequest,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        BeneficiaryService
        .add_beneficiary(
            db,
            current_user.Customer_CIF,
            request
        )
    )


@router.get("/my-beneficiaries")
def get_beneficiaries(
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        BeneficiaryService
        .get_beneficiaries(
            db,
            current_user.Customer_CIF
        )
    )

@router.delete("/{beneficiary_id}")
def delete_beneficiary(
    beneficiary_id: int,
    db: Session = Depends(get_db),
    current_user: LoginAuth = Depends(
        get_current_user
    )
):

    return (
        BeneficiaryService
        .delete_beneficiary(
            db,
            beneficiary_id,
            current_user.Customer_CIF
        )
    )