from datetime import datetime
from datetime import timedelta
from app.services.suspicious_activity_service import (
    SuspiciousActivityService
)
from app.repositories.fraud_repository import (
    FraudRepository
)

from app.models.transaction import (
    TransactionEntry
)


class FraudService:

    @staticmethod
    def check_large_transaction(
        db,
        account_no,
        transaction_id,
        amount
    ):

        if amount >= 100000:
            
            SuspiciousActivityService.log(
                db,
                account_no,
                transaction_id,
                "Large Transaction",
                "High",
                "Transaction amount exceeded threshold"
            )

            FraudRepository.create(
                db,
                account_no,
                transaction_id,
                90.00,
                "Large Transaction",
                "Transaction amount exceeded limit"
            )

    @staticmethod
    def check_transaction_frequency(
        db,
        account_no,
        transaction_id
    ):

        count = (
            db.query(TransactionEntry)
            .filter(
                TransactionEntry.Account_No
                == account_no,

                TransactionEntry.Entry_Time >=
                datetime.utcnow()
                - timedelta(minutes=5)
            )
            .count()
        )

        if count >= 5:
            
            SuspiciousActivityService.log(
                db,
                account_no,
                transaction_id,
                "High Frequency Transactions",
                "Medium",
                "More than 5 transactions in 5 minutes"
            )

            FraudRepository.create(
                db,
                account_no,
                transaction_id,
                70.00,
                "High Frequency",
                "Too many transactions in short period"
            )