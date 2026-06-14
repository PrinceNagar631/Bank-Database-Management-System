from pydantic import (
    BaseModel,
    EmailStr
)


class IndividualRegisterRequest(
    BaseModel
):

    username: str

    password: str

    pin: str

    email: EmailStr

    phone_no: str

    aadhaar: str

    pan: str

    first_name: str

    last_name: str

    gender: str

    dob: str