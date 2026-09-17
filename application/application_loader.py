from config.settings import bot_settings
from database.connection import get_connection


def get_candidate_profile_id() -> int:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT profile_id
                FROM candidate_profile
                ORDER BY profile_id DESC
                LIMIT 1;
                """
            )

            row = cursor.fetchone()

    if row is None:
        raise ValueError(
            "No candidate profile found in the database."
        )

    return row[0]


def create_application_records(profile_id: int) -> int:
    inserted_count = 0
    eligible_count = 0
    skipped_existing_count = 0

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    jm.job_id,
                    jm.match_score
                FROM job_matches jm
                INNER JOIN jobs j
                    ON j.job_id = jm.job_id
                WHERE jm.profile_id = %s
                  AND jm.match_status = 'APPLY'
                  AND j.status = 'FOUND'
                ORDER BY jm.match_score DESC;
                """,
                (profile_id,),
            )

            matched_jobs = cursor.fetchall()

            for job_id, match_score in matched_jobs:

                if float(match_score) < bot_settings.minimum_match_score:
                    continue

                eligible_count += 1

                cursor.execute(
                    """
                    SELECT
                        application_id,
                        application_status
                    FROM applications
                    WHERE job_id = %s
                      AND profile_id = %s
                    LIMIT 1;
                    """,
                    (
                        job_id,
                        profile_id,
                    ),
                )

                existing_application = cursor.fetchone()

                if existing_application is not None:
                    application_id, application_status = (
                        existing_application
                    )

                    skipped_existing_count += 1

                    print(
                        f"SKIP existing application | "
                        f"Job ID: {job_id} | "
                        f"Application ID: {application_id} | "
                        f"Status: {application_status}"
                    )

                    continue

                cursor.execute(
                    """
                    INSERT INTO applications (
                        job_id,
                        profile_id,
                        application_status
                    )
                    VALUES (
                        %s,
                        %s,
                        'READY'
                    )
                    ON CONFLICT (job_id, profile_id)
                    DO NOTHING;
                    """,
                    (
                        job_id,
                        profile_id,
                    ),
                )

                if cursor.rowcount == 1:
                    inserted_count += 1

                    print(
                        f"APPLICATION CREATED | "
                        f"Job ID: {job_id} | "
                        f"Status: READY"
                    )

    print("=" * 60)
    print("APPLICATION LOADER")
    print("=" * 60)
    print(f"Profile ID              : {profile_id}")
    print(f"Eligible matches        : {eligible_count}")
    print(f"Existing applications   : {skipped_existing_count}")
    print(f"New applications        : {inserted_count}")
    print("=" * 60)

    return inserted_count


if __name__ == "__main__":
    profile_id = get_candidate_profile_id()
    create_application_records(profile_id)