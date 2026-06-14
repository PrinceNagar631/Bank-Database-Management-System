from datetime import date

from app.models.account import Account
from app.models.daily_balance import DailyBalance
from app.repositories.daily_balance_repository import (
    DailyBalanceRepository
)


class DailyBalanceService:

    @staticmethod
    def snapshot_account(
        db,
        account_no
    ):

        account = (
            db.query(Account)
            .filter(
                Account.Account_No == account_no
            )
            .first()
        )

        if account is None:
            return

        DailyBalanceRepository.create(
            db=db,
            account_no=account.Account_No,
            balance_date=date.today(),
            closing_balance=account.Current_Balance
        )

    @staticmethod
    def update_balance(
        db,
        account_no,
        closing_balance
    ):
        record = (
            db.query(DailyBalance)
            .filter(
                DailyBalance.Account_No == account_no,
                DailyBalance.Balance_Date == date.today()
            )
            .first()
        )

        if record is None:
            record = DailyBalance(
                Account_No=account_no,
                Balance_Date=date.today(),
                Closing_Balance=closing_balance
            )
            db.add(record)
        else:
            record.Closing_Balance = closing_balance