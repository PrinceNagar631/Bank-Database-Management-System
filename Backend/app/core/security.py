from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from jose import JWTError
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.auth import LoginAuth
from app.models.login_session import LoginSession
import uuid

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(password: str):

    password = password[:72]

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    plain_password = plain_password[:72]

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    jti = str(uuid.uuid4())

    to_encode.update(
        {
            "exp": expire,
            "jti": jti
        }
    )

    token = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token, jti

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        username = payload.get("sub")

        jti = payload.get("jti")

        if username is None:

            raise credentials_exception

        if jti is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    session = (
        db.query(LoginSession)
        .filter(
            LoginSession.JWT_ID == jti,
            LoginSession.Session_Status == "Active"
        )
        .first()
    )

    if session is None:

        raise HTTPException(
            status_code=401,
            detail="Session invalid"
        )

    user = (
        db.query(LoginAuth)
        .filter(
            LoginAuth.User_ID == username
        )
        .first()
    )

    if user is None:

        raise credentials_exception

    return user