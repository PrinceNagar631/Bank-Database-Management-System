from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.suspicious_activity_service import (
    SuspiciousActivityService
)
from app.repositories.auth_repository import (
    AuthRepository
)
from app.repositories.login_history_repository import (
    LoginHistoryRepository
)
from app.services.audit_log_service import (
    AuditLogService
)
from app.core.security import (
    verify_password,
    create_access_token
)
from datetime import datetime, timedelta

from app.models.login_session import (
    LoginSession
)
from jose import jwt
from app.core.config import settings
from app.repositories.login_session_repository import (
    LoginSessionRepository
)
from app.core.config import settings

class AuthService:

    @staticmethod
    def login(
        db: Session,
        username: str,
        password: str,
        request
    ):

        user = AuthRepository.get_user(
            db,
            username
        )

        if not user:

            LoginHistoryRepository.create(
                db=db,
                user_id=username,
                status="Failed",
                ip_address=request.client.host,
                device_info=request.headers.get(
                    "user-agent"
                ),
                failure_reason="Invalid credentials"
            )

            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        valid_password = verify_password(
            password,
            user.Password_Hash
        )

        if not valid_password:

            LoginHistoryRepository.create(
                db=db,
                user_id=username,
                status="Failed",
                ip_address=request.client.host,
                device_info=request.headers.get(
                    "user-agent"
                ),
                failure_reason="Wrong password"
            )

            SuspiciousActivityService.log(
                db,
                None,
                None,
                "Failed Login",
                "Medium",
                f"Failed login attempt for {username}"
            )

            db.commit()

            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        db.query(LoginSession).filter(
            LoginSession.Expiry_Time < datetime.utcnow(),
            LoginSession.Session_Status == "Active"
        ).update(
            {
                "Session_Status": "Expired"
            },
            synchronize_session=False
        )

        db.commit()

        active_sessions = (
            db.query(LoginSession)
            .filter(
                LoginSession.User_ID == user.User_ID,
                LoginSession.Session_Status == "Active"
            )
            .count()
        )

        if active_sessions >= 3:

            SuspiciousActivityService.log(
                db,
                None,
                None,
                "Session Limit Exceeded",
                "Medium",
                f"User {username} exceeded active session limit"
            )

            db.commit()

            raise HTTPException(
                status_code=403,
                detail="Maximum active sessions reached"
            )

        access_token, jti = create_access_token(
            {
                "sub": user.User_ID
            }
        )

        session = LoginSession(
            User_ID=user.User_ID,
            JWT_ID=jti,
            IP_Address=request.client.host,
            Device_Info=request.headers.get(
                "user-agent"
            ),
            Expiry_Time=
            datetime.utcnow()
            + timedelta(
                minutes=
                settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
            Session_Status="Active"
        )

        db.add(session)

        LoginHistoryRepository.create(
            db=db,
            user_id=username,
            status="Success",
            ip_address=request.client.host,
            device_info=request.headers.get(
                "user-agent"
            )
        )

        AuditLogService.log(
            db,
            "Login_Auth",
            "UPDATE",
            user.User_ID,
            user.User_ID,
            None,
            {
                "event": "LOGIN"
            }
        )

        db.commit()

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    

    @staticmethod
    def logout(
        db,
        token
    ):

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ]
        )

        jti = payload.get("jti")

        session = (
            LoginSessionRepository
            .get_by_jti(
                db,
                jti
            )
        )

        if session:

            session.Session_Status = (
                "Logged_Out"
            )

            session.Logout_Time = (
                datetime.utcnow()
            )

            AuditLogService.log(
                db,
                "Login_Session",
                "UPDATE",
                str(session.Session_ID),
                session.User_ID,
                None,
                {
                    "event": "LOGOUT"
                }
            )

            db.commit()

        return {
            "message":
            "Logged out successfully"
        }