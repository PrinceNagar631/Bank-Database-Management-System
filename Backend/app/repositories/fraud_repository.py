from datetime import datetime
from app.models.fraud_flag import FraudFlag


class FraudRepository:

    @staticmethod
    def create(
        db,
        account_no,
        transaction_id,
        risk_score,
        flag_type,
        description
    ):

        fraud = FraudFlag(
            Account_No=account_no,
            Transaction_ID=transaction_id,
            Risk_Score=risk_score,
            Flag_Type=flag_type,
            Description=description,
            Investigation_Status="Open"
        )

        db.add(fraud)

        return fraud