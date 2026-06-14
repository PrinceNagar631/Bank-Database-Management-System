from datetime import datetime,timedelta
from decimal import Decimal
import uuid
from fastapi import HTTPException
from app.models.auth import LoginAuth
from app.models.account import (
    Account,
    AccountHolder
)
from app.services.daily_balance_service import (
    DailyBalanceService
)
from app.services.audit_log_service import AuditLogService
from app.services.fraud_service import FraudService
from app.models.transaction import (
    TransactionMaster,
    TransactionEntry
)


class TransactionService:

    @staticmethod
    def validate_account_ownership(
        db,
        account_no,
        customer_cif
    ):

        ownership = (
            db.query(AccountHolder)
            .filter(
                AccountHolder.Account_No == account_no,
                AccountHolder.CIF_No == customer_cif
            )
            .first()
        )

        if ownership is None:

            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this account"
            )

    @staticmethod
    def deposit(
        db,
        account_no,
        amount,
        username,
        customer_cif
    ):

        try:

            TransactionService.validate_account_ownership(
                db,
                account_no,
                customer_cif
            )

            account = (
                db.query(Account)
                .filter(
                    Account.Account_No == account_no
                )
                .with_for_update()
                .first()
            )

            if account is None:

                raise HTTPException(
                    status_code=404,
                    detail="Account not found"
                )

            amount = Decimal(str(amount))

            reference_number = str(
                uuid.uuid4()
            )

            transaction = TransactionMaster(
                Transaction_Type="Deposit",
                Transaction_Status="Pending",
                Initiated_By_User=username,
                Reference_Number=reference_number,
                Remarks="Cash Deposit"
            )

            db.add(transaction)

            db.flush()

            account.Current_Balance += amount

            account.Available_Balance += amount

            account.Last_Transaction_At = (
                datetime.utcnow()
            )

            entry = TransactionEntry(
                Transaction_ID=
                transaction.Transaction_ID,

                Account_No=
                account.Account_No,

                Entry_Type="Credit",

                Amount=amount,

                Balance_After=
                account.Current_Balance
            )

            db.add(entry)

            from app.services.fraud_service import (
                FraudService
            )

            FraudService.check_large_transaction(
                db,
                account.Account_No,
                transaction.Transaction_ID,
                amount
            )

            FraudService.check_transaction_frequency(
                db,
                account.Account_No,
                transaction.Transaction_ID
            )

            transaction.Transaction_Status = (
                "Success"
            )

            transaction.Completed_At = (
                datetime.utcnow()
            )

            AuditLogService.log(
                db,
                "Transaction_Master",
                "INSERT",
                transaction.Transaction_ID,
                username,
                None,
                f"Deposited {amount} to {account_no}"
            )

            DailyBalanceService.update_balance(
                db,
                account.Account_No,
                account.Current_Balance
            )

            db.commit()

            return {
                "message":
                "Deposit successful",

                "transaction_id":
                transaction.Transaction_ID,

                "reference_number":
                reference_number,

                "balance":
                float(
                    account.Current_Balance
                )
            }

        except HTTPException:

            raise

        except Exception as e:

            db.rollback()

            print(
                "DEPOSIT ERROR:",
                str(e)
            )

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    @staticmethod
    def withdraw(
        db,
        account_no,
        amount,
        username,
        customer_cif
    ):

        try:

            TransactionService.validate_account_ownership(
                db,
                account_no,
                customer_cif
            )

            account = (
                db.query(Account)
                .filter(
                    Account.Account_No == account_no
                )
                .with_for_update()
                .first()
            )

            if account is None:

                raise HTTPException(
                    status_code=404,
                    detail="Account not found"
                )

            amount = Decimal(str(amount))

            if account.Available_Balance < amount:

                raise HTTPException(
                    status_code=400,
                    detail="Insufficient balance"
                )

            reference_number = str(
                uuid.uuid4()
            )

            transaction = TransactionMaster(
                Transaction_Type="Withdrawal",
                Transaction_Status="Pending",
                Initiated_By_User=username,
                Reference_Number=reference_number,
                Remarks="Cash Withdrawal"
            )

            db.add(transaction)

            db.flush()

            account.Current_Balance -= amount

            account.Available_Balance -= amount

            account.Last_Transaction_At = (
                datetime.utcnow()
            )

            entry = TransactionEntry(
                Transaction_ID=
                transaction.Transaction_ID,

                Account_No=
                account.Account_No,

                Entry_Type="Debit",

                Amount=amount,

                Balance_After=
                account.Current_Balance
            )

            db.add(entry)

            from app.services.fraud_service import (
                FraudService
            )

            FraudService.check_large_transaction(
                db,
                account.Account_No,
                transaction.Transaction_ID,
                amount
            )

            FraudService.check_transaction_frequency(
                db,
                account.Account_No,
                transaction.Transaction_ID
            )

            transaction.Transaction_Status = (
                "Success"
            )

            transaction.Completed_At = (
                datetime.utcnow()
            )

            AuditLogService.log(
                db,
                "Transaction_Master",
                "INSERT",
                transaction.Transaction_ID,
                username,
                None,
                f"Withdrawn {amount} from {account_no}"
            )

            DailyBalanceService.update_balance(
                db,
                account.Account_No,
                account.Current_Balance
            )

            db.commit()

            return {
                "message":
                "Withdrawal successful",

                "transaction_id":
                transaction.Transaction_ID,

                "reference_number":
                reference_number,

                "balance":
                float(
                    account.Current_Balance
                )
            }

        except HTTPException:

            raise

        except Exception as e:

            db.rollback()

            print(
                "WITHDRAW ERROR:",
                str(e)
            )

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
        
    @staticmethod
    def transfer(
        db,
        from_account_no,
        to_account_no,
        amount,
        username,
        customer_cif
    ):
        user = (
            db.query(LoginAuth)
            .filter(
                LoginAuth.User_ID == username
            )
            .first()
        )

        if not user.OTP_Verified:

            raise HTTPException(
                status_code=403,
                detail="OTP verification required"
            )
        try:

            if from_account_no == to_account_no:

                raise HTTPException(
                    status_code=400,
                    detail="Cannot transfer to same account"
                )

            TransactionService.validate_account_ownership(
                db,
                from_account_no,
                customer_cif
            )

            amount = Decimal(str(amount))

            source_account = (
                db.query(Account)
                .filter(
                    Account.Account_No == from_account_no
                )
                .with_for_update()
                .first()
            )

            destination_account = (
                db.query(Account)
                .filter(
                    Account.Account_No == to_account_no
                )
                .with_for_update()
                .first()
            )

            if source_account is None:

                raise HTTPException(
                    status_code=404,
                    detail="Source account not found"
                )

            if destination_account is None:

                raise HTTPException(
                    status_code=404,
                    detail="Destination account not found"
                )

            if source_account.Available_Balance < amount:

                raise HTTPException(
                    status_code=400,
                    detail="Insufficient balance"
                )

            reference_number = str(
                uuid.uuid4()
            )

            transaction = TransactionMaster(
                Transaction_Type="Transfer",
                Transaction_Status="Pending",
                Initiated_By_User=username,
                Reference_Number=reference_number,
                Remarks="Account Transfer"
            )

            db.add(transaction)

            db.flush()

            source_account.Current_Balance -= amount
            source_account.Available_Balance -= amount

            destination_account.Current_Balance += amount
            destination_account.Available_Balance += amount

            now = datetime.utcnow()

            source_account.Last_Transaction_At = now
            destination_account.Last_Transaction_At = now

            debit_entry = TransactionEntry(
                Transaction_ID=
                transaction.Transaction_ID,

                Account_No=
                source_account.Account_No,

                Entry_Type="Debit",

                Amount=amount,

                Balance_After=
                source_account.Current_Balance
            )

            credit_entry = TransactionEntry(
                Transaction_ID=
                transaction.Transaction_ID,

                Account_No=
                destination_account.Account_No,

                Entry_Type="Credit",

                Amount=amount,

                Balance_After=
                destination_account.Current_Balance
            )

            db.add(debit_entry)
            db.add(credit_entry)

            FraudService.check_large_transaction(
                db,
                source_account.Account_No,
                transaction.Transaction_ID,
                amount
            )

            FraudService.check_transaction_frequency(
                db,
                source_account.Account_No,
                transaction.Transaction_ID
            )

            transaction.Transaction_Status = (
                "Success"
            )

            transaction.Completed_At = now

            user.OTP_Verified = False

            AuditLogService.log(
                db,
                "Transaction_Master",
                "INSERT",
                transaction.Transaction_ID,
                username,
                None,
                f"{amount} transferred from {from_account_no} to {to_account_no}"
            )

            DailyBalanceService.update_balance(
                db,
                source_account.Account_No,
                source_account.Current_Balance
            )

            DailyBalanceService.update_balance(
                db,
                destination_account.Account_No,
                destination_account.Current_Balance
            )

            db.commit()

            return {
                "message":
                "Transfer successful",

                "transaction_id":
                transaction.Transaction_ID,

                "reference_number":
                reference_number,

                "from_account":
                from_account_no,

                "to_account":
                to_account_no,

                "amount":
                float(amount)
            }

        except HTTPException:

            raise

        except Exception as e:

            db.rollback()

            print(
                "TRANSFER ERROR:",
                str(e)
            )

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
        
    @staticmethod
    def get_transaction_history(
        db,
        account_no,
        customer_cif
    ):

        TransactionService.validate_account_ownership(
            db,
            account_no,
            customer_cif
        )

        entries = (
            db.query(
                TransactionEntry
            )
            .filter(
                TransactionEntry.Account_No
                == account_no
            )
            .order_by(
                TransactionEntry.Entry_Time.desc()
            )
            .all()
        )

        result = []

        for entry in entries:

            result.append(
                {
                    "transaction_id":
                    entry.Transaction_ID,

                    "account_no":
                    entry.Account_No,

                    "entry_type":
                    entry.Entry_Type,

                    "amount":
                    float(entry.Amount),

                    "balance_after":
                    float(
                        entry.Balance_After
                    ),

                    "entry_time":
                    str(
                        entry.Entry_Time
                    )
                }
            )

        return result
    @staticmethod
    def get_mini_statement(
        db,
        account_no,
        customer_cif
    ):

        TransactionService.validate_account_ownership(
            db,
            account_no,
            customer_cif
        )

        entries = (
            db.query(TransactionEntry)
            .filter(
                TransactionEntry.Account_No
                == account_no
            )
            .order_by(
                TransactionEntry.Entry_Time.desc()
            )
            .limit(10)
            .all()
        )

        result = []

        for entry in entries:

            result.append(
                {
                    "transaction_id":
                    entry.Transaction_ID,

                    "entry_type":
                    entry.Entry_Type,

                    "amount":
                    float(entry.Amount),

                    "balance_after":
                    float(entry.Balance_After),

                    "entry_time":
                    str(entry.Entry_Time)
                }
            )

        return result
    
    @staticmethod
    def get_account_statement(
        db,
        account_no,
        from_date,
        to_date,
        customer_cif
    ):

        TransactionService.validate_account_ownership(
            db,
            account_no,
            customer_cif
        )

        entries = (
            db.query(TransactionEntry)
            .filter(
                TransactionEntry.Account_No == account_no,
                TransactionEntry.Entry_Time >= from_date,
                TransactionEntry.Entry_Time <
                (
                    to_date +
                    timedelta(days=1)
                )
            )
            .order_by(
                TransactionEntry.Entry_Time.desc()
            )
            .all()
        )

        result = []

        for entry in entries:

            result.append(
                {
                    "transaction_id":
                    entry.Transaction_ID,

                    "entry_type":
                    entry.Entry_Type,

                    "amount":
                    float(entry.Amount),

                    "balance_after":
                    float(entry.Balance_After),

                    "entry_time":
                    str(entry.Entry_Time)
                }
            )

        return result