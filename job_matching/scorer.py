from config.profile import candidate_profile
from job_matching.skill_matcher import find_skill_match


def calculate_match_score(job: dict) -> dict:

    result = find_skill_match(
        job,
        candidate_profile.core_skills,
        candidate_profile.additional_skills,
    )

    core_matched = result["core_matched"]
    additional_matched = result["additional_matched"]

    # ---------------------------------------------------------
    # 1. CORE SKILLS SCORE - 50%
    # ---------------------------------------------------------
    if candidate_profile.core_skills:
        core_score = (
            len(core_matched)
            / len(candidate_profile.core_skills)
            * 50
        )
    else:
        core_score = 0

    # ---------------------------------------------------------
    # 2. ADDITIONAL SKILLS SCORE - 10%
    # ---------------------------------------------------------
    if candidate_profile.additional_skills:
        additional_score = (
            len(additional_matched)
            / len(candidate_profile.additional_skills)
            * 10
        )
    else:
        additional_score = 0

    # ---------------------------------------------------------
    # 3. ROLE SCORE - 15%
    # ---------------------------------------------------------
    title = str(
        job.get("job_title", "")
    ).lower()

    role_match = any(
        role.lower() in title
        for role in candidate_profile.target_roles
    )

    role_score = 15 if role_match else 0

    # ---------------------------------------------------------
    # 4. LOCATION SCORE - 10%
    # ---------------------------------------------------------
    location = str(
        job.get("location", "")
    ).lower()

    location_match = any(
        preferred.lower() in location
        for preferred in candidate_profile.preferred_locations
    )

    location_score = 10 if location_match else 0

    # ---------------------------------------------------------
    # 5. EXPERIENCE MATCH - 15%
    # ---------------------------------------------------------
    experience_match = False

    try:
        job_min = float(job.get("experience_min"))
        job_max = float(job.get("experience_max"))

        candidate_min = float(
            candidate_profile.experience_min
        )
        candidate_max = float(
            candidate_profile.experience_max
        )

        experience_match = (
            job_min <= candidate_max
            and job_max >= candidate_min
        )

    except (TypeError, ValueError):
        experience_match = False

    experience_score = 15 if experience_match else 0

    # ---------------------------------------------------------
    # TOTAL SCORE
    # ---------------------------------------------------------
    total_score = (
        core_score
        + additional_score
        + role_score
        + location_score
        + experience_score
    )

    # ---------------------------------------------------------
    # HARD EXPERIENCE GATE
    #
    # If the job experience range does NOT overlap with the
    # candidate's experience range, the job cannot qualify.
    # ---------------------------------------------------------
    if not experience_match:
        total_score = 0

    return {
        "match_score": round(total_score, 2),
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "role_match": role_match,
        "location_match": location_match,
        "experience_match": experience_match,
    }