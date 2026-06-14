from app.repositories.suspicious_activity_repository import (
    SuspiciousActivityRepository
)


class SuspiciousActivityService:

    @staticmethod
    def log(
        db,
        account_no,
        transaction_id,
        activity_type,
        risk_level,
        description
    ):

        SuspiciousActivityRepository.create(
            db,
            account_no,
            transaction_id,
            activity_type,
            risk_level,
            description
        )