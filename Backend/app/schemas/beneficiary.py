from pydantic import BaseModel


class AddBeneficiaryRequest(BaseModel):

    nickname: str

    beneficiary_name: str

    beneficiary_account_no: int

    beneficiary_ifsc: str


class BeneficiaryResponse(BaseModel):

    beneficiary_id: int

    nickname: str

    beneficiary_name: str

    beneficiary_account_no: int

    beneficiary_ifsc: str

    status: str