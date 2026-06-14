from pydantic import BaseModel


class CreateSavingsAccountRequest(BaseModel):

    branch_id: int


class CreateCurrentAccountRequest(BaseModel):

    branch_id: int