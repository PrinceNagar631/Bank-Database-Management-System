from app.models.suspicious_activity_log import (
    SuspiciousActivityLog
)


class SuspiciousActivityRepository:

    @staticmethod
    def create(
        db,
        account_no,
        transaction_id,
        activity_type,
        risk_level,
        description
    ):

        log = SuspiciousActivityLog(
            Account_No=account_no,
            Transaction_ID=transaction_id,
            Activity_Type=activity_type,
            Risk_Level=risk_level,
            Description=description
        )

        db.add(log)

        return log