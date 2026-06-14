from sqlalchemy.orm import Session


class AccountRepository:

    @staticmethod
    def add(
        db: Session,
        obj
    ):
        db.add(obj)