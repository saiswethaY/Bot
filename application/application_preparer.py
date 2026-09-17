from database.connection import get_connection


def get_ready_applications() -> list[int]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT application_id
                FROM applications
                WHERE application_status = 'READY'
                ORDER BY application_id;
                """
            )

            rows = cursor.fetchall()

    return [row[0] for row in rows]


def prepare_application(application_id: int) -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE applications
                SET
                    resume_version = 'resume_v1',
                    cover_letter_version = 'cover_letter_v1',
                    updated_at = CURRENT_TIMESTAMP
                WHERE application_id = %s
                  AND application_status = 'READY';
                """,
                (application_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Application {application_id} "
                    f"not found or application is not READY."
                )


def prepare_all_applications() -> None:
    application_ids = get_ready_applications()

    if not application_ids:
        print("No READY applications found.")
        return

    print("=" * 60)
    print("APPLICATION PREPARATION")
    print("=" * 60)
    print(f"READY applications : {len(application_ids)}")
    print()

    prepared_count = 0

    for application_id in application_ids:
        prepare_application(application_id)

        prepared_count += 1

        print(
            f"Application {application_id} "
            f"prepared successfully."
        )

    print()
    print(f"Applications prepared : {prepared_count}")
    print("=" * 60)


if __name__ == "__main__":
    prepare_all_applications()