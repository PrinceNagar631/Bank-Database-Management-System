from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware
)
from app.models.branch import Branch
from app.api import (
    auth_routes,
    test_routes,
    user_routes,
    customer_routes,
    account_routes,
    transaction_routes,
    beneficiary_routes,
    otp_routes,
    fraud_routes,
    suspicious_activity_routes,
    audit_routes,
    daily_balance_routes,
    interest_routes,
    loan_routes
)
from app.models.transaction import (
    TransactionMaster,
    TransactionEntry
)

app = FastAPI(
    title="Bank API"
)

app.include_router(
    test_routes.router
)
app.include_router(
    user_routes.router
)
app.include_router(
    customer_routes.router
)
app.include_router(
    account_routes.router
)
app.include_router(
    transaction_routes.router
)
app.include_router(
    beneficiary_routes.router
)
app.include_router(
    otp_routes.router
)
app.include_router(
    fraud_routes.router
)
app.include_router(
    suspicious_activity_routes.router
)
app.include_router(
    audit_routes.router
)
app.include_router(
    daily_balance_routes.router
)
app.include_router(
    interest_routes.router
)
app.include_router(
    loan_routes.router
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_routes.router
)


@app.get("/")
def root():

    return {
        "message": "Bank API Running"
    }