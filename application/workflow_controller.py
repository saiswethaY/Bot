from application.application_workflow import (
    ApplicationState,
)
from database.connection import get_connection


def get_application(application_id: int) -> dict:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    application_id,
                    job_id,
                    profile_id,
                    application_status,
                    resume_version,
                    cover_letter_version
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

    return {
        "application_id": row[0],
        "job_id": row[1],
        "profile_id": row[2],
        "application_status": row[3],
        "resume_version": row[4],
        "cover_letter_version": row[5],
    }


def start_application_workflow(
    application_id: int,
) -> ApplicationState:

    application = get_application(application_id)

    if application["application_status"] != "READY":
        raise ValueError(
            "Application is not READY for workflow processing."
        )

    return ApplicationState.READY


if __name__ == "__main__":
    state = start_application_workflow(1)
    print(f"Workflow started in state: {state.value}")