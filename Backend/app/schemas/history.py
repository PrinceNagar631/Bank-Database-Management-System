from pydantic import BaseModel


class TransactionHistoryResponse(
    BaseModel
):
    transaction_id: int
    account_no: int
    entry_type: str
    amount: float
    balance_after: float
    entry_time: str