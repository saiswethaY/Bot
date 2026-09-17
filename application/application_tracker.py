from application.status_transition import (
    validate_status_transition,
)
from database.connection import get_connection


VALID_STATUSES = {
    "READY",
    "IN_PROGRESS",
    "PAUSED",
    "FAILED",
    "SUBMITTED",
}


def update_application_status(
    application_id: int,
    new_status: str,
    failure_reason: str | None = None,
) -> None:

    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid application status: {new_status}"
        )

    if new_status == "FAILED":
        if not failure_reason or not failure_reason.strip():
            raise ValueError(
                "Failure reason is required when status is FAILED."
            )

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT application_status
                FROM applications
                WHERE application_id = %s;
                """,
                (application_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise ValueError(
                    f"Application {application_id} not found."
                )

            current_status = row[0]

            validate_status_transition(
                current_status,
                new_status,
            )

            if new_status == "SUBMITTED":

                cursor.execute(
                    """
                    UPDATE applications
                    SET
                        application_status = %s,
                        applied_at = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE application_id = %s;
                    """,
                    (
                        new_status,
                        application_id,
                    ),
                )

            elif new_status == "FAILED":

                cursor.execute(
                    """
                    UPDATE applications
                    SET
                        application_status = %s,
                        failure_reason = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE application_id = %s;
                    """,
                    (
                        new_status,
                        failure_reason.strip(),
                        application_id,
                    ),
                )

            else:

                cursor.execute(
                    """
                    UPDATE applications
                    SET
                        application_status = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE application_id = %s;
                    """,
                    (
                        new_status,
                        application_id,
                    ),
                )