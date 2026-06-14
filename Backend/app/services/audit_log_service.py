from app.repositories.audit_log_repository import (
    AuditLogRepository
)


class AuditLogService:

    @staticmethod
    def log(
        db,
        table_name,
        operation_type,
        record_primary_key,
        performed_by,
        old_value=None,
        new_value=None
    ):

        AuditLogRepository.create(
            db,
            table_name,
            operation_type,
            record_primary_key,
            performed_by,
            old_value,
            new_value
        )