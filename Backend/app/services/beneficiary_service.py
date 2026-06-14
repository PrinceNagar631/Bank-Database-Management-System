from fastapi import HTTPException

from app.models.beneficiary import (
    Beneficiary
)


class BeneficiaryService:

    @staticmethod
    def add_beneficiary(
        db,
        customer_cif,
        request
    ):

        existing = (
            db.query(Beneficiary)
            .filter(
                Beneficiary.Owner_CIF
                == customer_cif,

                Beneficiary
                .Beneficiary_Account_No
                ==
                request.beneficiary_account_no
            )
            .first()
        )

        if existing:

            raise HTTPException(
                status_code=400,
                detail="Beneficiary already exists"
            )

        beneficiary = Beneficiary(
            Owner_CIF=customer_cif,

            Nickname=request.nickname,

            Beneficiary_Name=
            request.beneficiary_name,

            Beneficiary_Account_No=
            request.beneficiary_account_no,

            Beneficiary_IFSC=
            request.beneficiary_ifsc,

            Status="Active"
        )

        db.add(beneficiary)

        db.commit()

        db.refresh(beneficiary)

        return {
            "message":
            "Beneficiary added",

            "beneficiary_id":
            beneficiary.Beneficiary_ID
        }

    @staticmethod
    def get_beneficiaries(
        db,
        customer_cif
    ):

        beneficiaries = (
            db.query(Beneficiary)
            .filter(
                Beneficiary.Owner_CIF
                == customer_cif
            )
            .all()
        )

        result = []

        for b in beneficiaries:

            result.append({

                "beneficiary_id":
                b.Beneficiary_ID,

                "nickname":
                b.Nickname,

                "beneficiary_name":
                b.Beneficiary_Name,

                "beneficiary_account_no":
                b.Beneficiary_Account_No,

                "beneficiary_ifsc":
                b.Beneficiary_IFSC,

                "status":
                b.Status
            })

        return result
    @staticmethod
    def delete_beneficiary(
        db,
        beneficiary_id,
        customer_cif
    ):

        beneficiary = (
            db.query(Beneficiary)
            .filter(
                Beneficiary.Beneficiary_ID
                == beneficiary_id,

                Beneficiary.Owner_CIF
                == customer_cif
            )
            .first()
        )

        if beneficiary is None:

            raise HTTPException(
                status_code=404,
                detail="Beneficiary not found"
            )

        db.delete(beneficiary)

        db.commit()

        return {
            "message":
            "Beneficiary deleted"
        }