from application.application_tracker import (
    update_application_status,
)
from database.connection import get_connection


def main():
    application_id = 1

    update_application_status(
        application_id,
        "FAILED",
        "Application form submission failed during validation.",
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    application_id,
                    application_status,
                    failure_reason
                FROM applications
                WHERE application_id = %s;
                """,
                (application_id,),
            )

            row = cursor.fetchone()

    if row is None:
        raise ValueError("Application was not found.")

    print("=" * 50)
    print("FAILED STATUS TEST")
    print("=" * 50)
    print(f"Application ID : {row[0]}")
    print(f"Status         : {row[1]}")
    print(f"Failure Reason : {row[2]}")
    print("=" * 50)


if __name__ == "__main__":
    main()