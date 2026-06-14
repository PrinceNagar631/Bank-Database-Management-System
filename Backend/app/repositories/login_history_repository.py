from app.models.login_history import LoginHistory


class LoginHistoryRepository:

    @staticmethod
    def create(
        db,
        user_id,
        status,
        ip_address=None,
        device_info=None,
        failure_reason=None
    ):

        history = LoginHistory(
            User_ID=user_id,
            Login_Status=status,
            IP_Address=ip_address,
            Device_Info=device_info,
            Failure_Reason=failure_reason
        )

        db.add(history)

        db.commit()

        return history