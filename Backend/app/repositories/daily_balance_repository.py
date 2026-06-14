from app.models.daily_balance import DailyBalance


class DailyBalanceRepository:

    @staticmethod
    def create(
        db,
        account_no,
        balance_date,
        closing_balance
    ):

        row = DailyBalance(
            Account_No=account_no,
            Balance_Date=balance_date,
            Closing_Balance=closing_balance
        )

        db.add(row)
        db.commit()

        return row