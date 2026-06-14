from pydantic import BaseModel


class LoanApplyRequest(BaseModel):

    branch_id: int
    loan_type: str
    principal_amount: float
    interest_rate: float
    loan_term_months: int