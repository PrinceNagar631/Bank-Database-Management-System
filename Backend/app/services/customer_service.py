from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.customer import (
    Customer,
    IndividualCustomer
)

from app.models.auth import (
    LoginAuth
)

from app.repositories.customer_repository import (
    CustomerRepository
)

from app.core.security import (
    hash_password
)


class CustomerService:

    @staticmethod
    def register_individual(
        db: Session,
        request
    ):

        existing_email = (
            db.query(Customer)
            .filter(
                Customer.Email == request.email
            )
            .first()
        )

        if existing_email:

            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        existing_user = (
            db.query(LoginAuth)
            .filter(
                LoginAuth.User_ID == request.username
            )
            .first()
        )

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        try:

            customer = Customer(
                Customer_Type="Individual",
                Email=request.email,
                Phone_No=request.phone_no
            )

            CustomerRepository.create_customer(
                db,
                customer
            )

            db.flush()

            individual = IndividualCustomer(
                CIF_No=customer.CIF_No,
                Aadhaar=request.aadhaar,
                PAN=request.pan,
                First_Name=request.first_name,
                Last_Name=request.last_name,
                Gender=request.gender,
                DOB=request.dob
            )

            CustomerRepository.create_individual(
                db,
                individual
            )

            login = LoginAuth(
                User_ID=request.username,
                Customer_CIF=customer.CIF_No,
                Password_Hash=hash_password(
                    request.password
                ),
                PIN_Hash=hash_password(
                    request.pin
                )
            )

            CustomerRepository.create_login(
                db,
                login
            )

            db.commit()

            return {
                "message": "Customer created successfully",
                "cif_no": customer.CIF_No
            }

        except Exception as e:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )