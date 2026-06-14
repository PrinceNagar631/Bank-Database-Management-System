from datetime import datetime

from app.models.daily_balance import DailyBalance
from app.models.interest_accrual import InterestAccrual


class InterestAccrualService:

    @staticmethod
    def create_interest(
        db,
        account_no,
        start_date,
        end_date,
        annual_rate
    ):

        balances = (
            db.query(DailyBalance)
            .filter(
                DailyBalance.Account_No == account_no,
                DailyBalance.Balance_Date >= start_date,
                DailyBalance.Balance_Date <= end_date
            )
            .all()
        )

        if not balances:
            return None

        average_balance = (
            sum(
                float(b.Closing_Balance)
                for b in balances
            )
            / len(balances)
        )

        interest_amount = (
            average_balance
            * float(annual_rate)
            / 100
            / 12
        )

        accrual = InterestAccrual(
            Account_No=account_no,
            Accrual_Start_Date=start_date,
            Accrual_End_Date=end_date,
            Average_Balance=average_balance,
            Interest_Rate=annual_rate,
            Interest_Amount=round(
                interest_amount,
                2
            ),
            Posted_Status="Pending"
        )

        db.add(accrual)
        db.commit()

        return accrual