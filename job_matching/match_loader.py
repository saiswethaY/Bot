import json

from config.settings import bot_settings
from database.connection import get_connection


def save_job_match(
    job_id: int,
    profile_id: int,
    match_result: dict,
) -> None:

    match_score = float(
        match_result["match_score"]
    )

    match_status = (
        "APPLY"
        if match_score >= bot_settings.minimum_match_score
        else "SKIP"
    )

    matched_skills = json.dumps(
        match_result["matched_skills"]
    )

    missing_skills = json.dumps(
        match_result["missing_skills"]
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:

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
                VALUES (%s, %s, %s, %s, %s, %s)

                ON CONFLICT (job_id, profile_id)
                DO UPDATE SET
                    match_score = EXCLUDED.match_score,
                    matched_skills = EXCLUDED.matched_skills,
                    missing_skills = EXCLUDED.missing_skills,
                    match_status = EXCLUDED.match_status,
                    evaluated_at = CURRENT_TIMESTAMP;
                """,
                (
                    job_id,
                    profile_id,
                    match_score,
                    matched_skills,
                    missing_skills,
                    match_status,
                ),
            )