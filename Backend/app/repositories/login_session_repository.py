from app.models.login_session import LoginSession


class LoginSessionRepository:

    @staticmethod
    def get_by_jti(
        db,
        jti
    ):
        return (
            db.query(LoginSession)
            .filter(
                LoginSession.JWT_ID == jti
            )
            .first()
        )