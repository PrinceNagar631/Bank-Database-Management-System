from sqlalchemy.orm import Session

from app.models.customer import (
    Customer,
    IndividualCustomer
)

from app.models.auth import (
    LoginAuth
)


class CustomerRepository:

    @staticmethod
    def create_customer(
        db: Session,
        customer: Customer
    ):
        db.add(customer)

    @staticmethod
    def create_individual(
        db: Session,
        individual: IndividualCustomer
    ):
        db.add(individual)

    @staticmethod
    def create_login(
        db: Session,
        login: LoginAuth
    ):
        db.add(login)