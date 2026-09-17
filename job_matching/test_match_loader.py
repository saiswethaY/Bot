from job_matching.scorer import calculate_match_score
from job_matching.match_loader import save_job_match
from database.connection import get_connection


def main():
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
                WHERE job_id = 1;
                """
            )

            job_row = cursor.fetchone()

            if job_row is None:
                raise ValueError("Job ID 1 was not found.")

            cursor.execute(
                """
                SELECT profile_id
                FROM candidate_profile
                ORDER BY profile_id
                LIMIT 1;
                """
            )

            profile_row = cursor.fetchone()

            if profile_row is None:
                raise ValueError(
                    "No candidate profile was found."
                )

    job = {
        "job_id": job_row[0],
        "job_title": job_row[1],
        "company_name": job_row[2],
        "location": job_row[3],
        "experience_min": job_row[4],
        "experience_max": job_row[5],
        "description": job_row[6],
    }

    profile_id = profile_row[0]

    match_result = calculate_match_score(job)

    save_job_match(
        job_id=job["job_id"],
        profile_id=profile_id,
        match_result=match_result,
    )

    print("=" * 50)
    print("MATCH SAVED")
    print("=" * 50)

    print(f"Job ID       : {job['job_id']}")
    print(f"Profile ID   : {profile_id}")
    print(f"Match Score  : {match_result['match_score']}%")
    print(
        f"Decision     : "
        f"{'APPLY' if match_result['match_score'] >= 70 else 'SKIP'}"
    )

    print("=" * 50)


if __name__ == "__main__":
    main()