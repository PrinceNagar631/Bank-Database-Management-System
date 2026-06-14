from sqlalchemy.orm import Session


class TransactionRepository:

    @staticmethod
    def add(
        db: Session,
        obj
    ):
        db.add(obj)