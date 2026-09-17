from database.connection import get_connection


def get_job_url(application_id: int) -> str:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    j.job_url
                FROM applications a
                JOIN jobs j
                    ON a.job_id = j.job_id
                WHERE a.application_id = %s;
                """,
                (application_id,),
            )

            row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"No job URL found for application {application_id}."
        )

    job_url = row[0]

    if not job_url.strip():
        raise ValueError(
            f"Job URL is empty for application {application_id}."
        )

    return job_url


if __name__ == "__main__":
    application_id = 1

    url = get_job_url(application_id)

    print("=" * 50)
    print("JOB URL RESOLVER TEST")
    print("=" * 50)
    print(f"Application ID : {application_id}")
    print(f"Job URL        : {url}")
    print("=" * 50)