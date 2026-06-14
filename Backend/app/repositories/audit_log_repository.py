from app.models.audit_log import AuditLog


class AuditLogRepository:

    @staticmethod
    def create(
        db,
        table_name,
        operation_type,
        record_primary_key,
        performed_by,
        old_value=None,
        new_value=None
    ):

        log = AuditLog(
            Table_Name=table_name,
            Operation_Type=operation_type,
            Record_Primary_Key=record_primary_key,
            Performed_By=performed_by,
            Old_Value=old_value,
            New_Value=new_value
        )

        db.add(log)

        return log