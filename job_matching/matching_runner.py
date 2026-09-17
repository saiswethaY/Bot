from config.settings import bot_settings
from database.connection import get_connection
from job_matching.decision import make_application_decision
from job_matching.match_loader import save_job_match
from job_matching.scorer import calculate_match_score


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


def get_jobs():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    job_id,
                    job_title,
                    company_name,
                    location,
                    experience_min,
                    experience_max,
                    description
                FROM jobs
                WHERE status = 'FOUND'
                ORDER BY job_id;
                """
            )

            rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append(
            {
                "job_id": row[0],
                "job_title": row[1],
                "company_name": row[2],
                "location": row[3],
                "experience_min": row[4],
                "experience_max": row[5],
                "description": row[6],
            }
        )

    return jobs


def run_matching():
    profile_id = get_candidate_profile_id()
    jobs = get_jobs()

    if not jobs:
        print("No jobs available for matching.")
        return

    print("=" * 60)
    print("JOB MATCHING RUN")
    print("=" * 60)

    print(f"Jobs to evaluate : {len(jobs)}")
    print(f"Profile ID       : {profile_id}")
    print(
        f"Minimum score    : {bot_settings.minimum_match_score}%"
    )
    print()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        for job in jobs:

            match_result = calculate_match_score(job)

            decision = make_application_decision(
                match_result["match_score"]
            )

            # Save the matching result
            save_job_match(
                job_id=job["job_id"],
                profile_id=profile_id,
                match_result=match_result,
            )

            # Queue matching jobs for application
            if decision == "APPLY":

                cursor.execute(
                    """
                    SELECT application_id
                    FROM applications
                    WHERE job_id = %s
                      AND profile_id = %s;
                    """,
                    (
                        job["job_id"],
                        profile_id,
                    ),
                )

                existing_application = cursor.fetchone()

                if existing_application is None:

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
                        );
                        """,
                        (
                            job["job_id"],
                            profile_id,
                        ),
                    )

                    connection.commit()

                    print(
                        f"Application queued | "
                        f"{job['job_title']} | "
                        f"{job['company_name']} | "
                        f"READY"
                    )

                else:

                    print(
                        f"Application already exists | "
                        f"{job['job_title']} | "
                        f"{job['company_name']}"
                    )

            print(
                f"{job['job_title']} | "
                f"{job['company_name']} | "
                f"{match_result['match_score']}% | "
                f"{decision}"
            )

    finally:
        cursor.close()
        connection.close()

    print()
    print("Matching completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    run_matching()