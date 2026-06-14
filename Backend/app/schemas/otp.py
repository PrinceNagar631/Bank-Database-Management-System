from pydantic import BaseModel


class GenerateOTPRequest(BaseModel):

    purpose: str


class VerifyOTPRequest(BaseModel):

    otp: str

    purpose: str