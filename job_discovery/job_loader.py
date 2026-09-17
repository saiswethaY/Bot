from database.connection import get_connection


def load_jobs(jobs: list[dict]) -> int:
    inserted_count = 0

    with get_connection() as connection:
        with connection.cursor() as cursor:

            for job in jobs:

                cursor.execute(
                    """
                    INSERT INTO jobs (
                        source,
                        external_job_id,
                        job_title,
                        company_name,
                        location,
                        experience_min,
                        experience_max,
                        job_url,
                        description,
                        posted_at
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (source, external_job_id)
                    DO UPDATE SET
                        job_title = EXCLUDED.job_title,
                        company_name = EXCLUDED.company_name,
                        location = EXCLUDED.location,
                        experience_min = EXCLUDED.experience_min,
                        experience_max = EXCLUDED.experience_max,
                        job_url = EXCLUDED.job_url,
                        description = EXCLUDED.description,
                        posted_at = EXCLUDED.posted_at
                    RETURNING job_id, (xmax = 0) AS inserted;
                    """,
                    (
                        job["source"],
                        job["external_job_id"],
                        job["job_title"],
                        job["company_name"],
                        job["location"],
                        job["experience_min"],
                        job["experience_max"],
                        job["job_url"],
                        job["description"],
                        job.get("posted_at"),
                    ),
                )

                result = cursor.fetchone()

                if result is not None and result[1]:
                    inserted_count += 1

    return inserted_count