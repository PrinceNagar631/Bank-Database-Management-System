from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.customer import (
    IndividualRegisterRequest
)

from app.services.customer_service import (
    CustomerService
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/register-individual"
)
def register_individual(
    request: IndividualRegisterRequest,
    db: Session = Depends(get_db)
):

    return CustomerService.register_individual(
        db,
        request
    )