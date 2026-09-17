from application.application_loader import create_application_records
from database.connection import get_connection


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            # Get the candidate profile
            cursor.execute(
                """
                SELECT profile_id
                FROM candidate_profile
                ORDER BY profile_id DESC
                LIMIT 1;
                """
            )

            profile_row = cursor.fetchone()

            if profile_row is None:
                raise ValueError("No candidate profile found.")

            profile_id = profile_row[0]

            # Get one existing job for controlled testing
            cursor.execute(
                """
                SELECT job_id
                FROM jobs
                ORDER BY job_id
                LIMIT 1;
                """
            )

            job_row = cursor.fetchone()

            if job_row is None:
                raise ValueError("No job found.")

            job_id = job_row[0]

            # Temporarily create an APPLY match
            cursor.execute(
                """
                INSERT INTO job_matches (
                    job_id,
                    profile_id,
                    match_score,
                    matched_skills,
                    missing_skills,
                    match_status
                )
                VALUES (
                    %s,
                    %s,
                    85,
                    '["SQL", "Python", "PySpark"]',
                    '[]',
                    'APPLY'
                )
                ON CONFLICT (job_id, profile_id)
                DO UPDATE SET
                    match_score = 85,
                    match_status = 'APPLY';
                """,
                (job_id, profile_id),
            )

    # Create the application record
    inserted_count = create_application_records(profile_id)

    print("=" * 50)
    print("POSITIVE APPLICATION TEST")
    print("=" * 50)
    print(f"Profile ID       : {profile_id}")
    print(f"Job ID           : {job_id}")
    print(f"Records inserted : {inserted_count}")
    print("=" * 50)


if __name__ == "__main__":
    main()