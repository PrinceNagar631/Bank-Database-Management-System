from datetime import date

from fastapi import HTTPException

from app.models.account import (
    Account,
    AccountHolder,
    SavingsAccount,
    CurrentAccount
)

from app.repositories.account_repository import (
    AccountRepository
)


class AccountService:

    @staticmethod
    def create_savings_account(
        db,
        branch_id,
        customer_cif
    ):

        try:

            account = Account(
                Branch_ID=branch_id,
                Account_Type="Savings",
                Account_Status="Active",
                Open_Date=date.today()
            )

            AccountRepository.add(
                db,
                account
            )

            db.flush()

            holder = AccountHolder(
                Account_No=account.Account_No,
                CIF_No=customer_cif,
                Holder_Type="Primary"
            )

            AccountRepository.add(
                db,
                holder
            )

            savings = SavingsAccount(
                Account_No=account.Account_No
            )

            AccountRepository.add(
                db,
                savings
            )

            db.commit()

            return {
                "message":
                "Savings account created",

                "account_no":
                account.Account_No
            }

        except Exception as e:

            db.rollback()

            print("ACCOUNT ERROR:", e)

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    @staticmethod
    def create_current_account(
        db,
        branch_id,
        customer_cif
    ):

        try:

            account = Account(
                Branch_ID=branch_id,
                Account_Type="Current",
                Account_Status="Active",
                Open_Date=date.today()
            )

            AccountRepository.add(
                db,
                account
            )

            db.flush()

            holder = AccountHolder(
                Account_No=account.Account_No,
                CIF_No=customer_cif,
                Holder_Type="Primary"
            )

            AccountRepository.add(
                db,
                holder
            )

            current = CurrentAccount(
                Account_No=account.Account_No
            )

            AccountRepository.add(
                db,
                current
            )

            db.commit()

            return {
                "message":
                "Current account created",

                "account_no":
                account.Account_No
            }

        except Exception as e:

            db.rollback()

            print("ACCOUNT ERROR:", e)

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
        
    @staticmethod
    def get_my_accounts(
        db,
        customer_cif
    ):

        accounts = (
            db.query(Account)
            .join(
                AccountHolder,
                Account.Account_No ==
                AccountHolder.Account_No
            )
            .filter(
                AccountHolder.CIF_No ==
                customer_cif
            )
            .all()
        )

        result = []

        for account in accounts:

            result.append(
                {
                    "account_no":
                    account.Account_No,

                    "account_type":
                    account.Account_Type,

                    "balance":
                    float(
                        account.Current_Balance
                    ),

                    "status":
                    account.Account_Status
                }
            )

        return result