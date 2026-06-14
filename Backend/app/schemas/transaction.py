from pydantic import BaseModel
from decimal import Decimal

class DepositRequest(BaseModel):
    account_no: int
    amount: Decimal


class WithdrawRequest(BaseModel):
    account_no: int
    amount: Decimal


class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: Decimal