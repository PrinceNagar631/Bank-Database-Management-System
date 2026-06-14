from app.models.loan import Loan
from datetime import date
from fastapi import HTTPException

class LoanService:

    @staticmethod
    def apply(
        db,
        customer_cif,
        request
    ):

        loan = Loan(
            Borrower_CIF=customer_cif,
            Branch_ID=request.branch_id,
            Loan_Type=request.loan_type,
            Loan_Status="Pending",
            Principal_Amount=request.principal_amount,
            Outstanding_Principal=request.principal_amount,
            Interest_Rate=request.interest_rate,
            Loan_Term_Months=request.loan_term_months
        )

        db.add(loan)
        db.commit()
        db.refresh(loan)

        return {
            "message": "Loan application submitted",
            "loan_id": loan.Loan_ID
        }

    @staticmethod
    def get_my_loans(
        db,
        customer_cif
    ):

        return (
            db.query(Loan)
            .filter(
                Loan.Borrower_CIF == customer_cif
            )
            .all()
        )
        
    @staticmethod
    def approve_loan(
        db,
        loan_id
    ):

        loan = (
            db.query(Loan)
            .filter(
                Loan.Loan_ID == loan_id
            )
            .first()
        )

        if loan is None:
            raise HTTPException(
                status_code=404,
                detail="Loan not found"
            )

        loan.Loan_Status = "Active"
        loan.Start_Date = date.today()

        db.commit()

        return {
            "message": "Loan approved"
        }


    @staticmethod
    def reject_loan(
        db,
        loan_id
    ):

        loan = (
            db.query(Loan)
            .filter(
                Loan.Loan_ID == loan_id
            )
            .first()
        )

        if loan is None:
            raise HTTPException(
                status_code=404,
                detail="Loan not found"
            )

        loan.Loan_Status = "Rejected"

        db.commit()

        return {
            "message": "Loan rejected"
        }