from config.profile import candidate_profile
from database.connection import get_connection


def seed_candidate_profile():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO candidate_profile (
                    profile_name,
                    experience_min,
                    experience_max,
                    notice_period_days
                )
                VALUES (%s, %s, %s, %s)
                RETURNING profile_id;
                """,
                (
                    "Swetha",
                    candidate_profile.experience_min,
                    candidate_profile.experience_max,
                    candidate_profile.notice_period_days,
                ),
            )

            profile_id = cursor.fetchone()[0]

    print("Candidate profile inserted successfully.")
    print(f"Profile ID: {profile_id}")


if __name__ == "__main__":
    seed_candidate_profile()