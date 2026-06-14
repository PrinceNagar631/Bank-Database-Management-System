from sqlalchemy.orm import Session

from app.models.auth import LoginAuth


class AuthRepository:

    @staticmethod
    def get_user(
        db: Session,
        username: str
    ):

        return (
            db.query(LoginAuth)
            .filter(
                LoginAuth.User_ID == username
            )
            .first()
        )