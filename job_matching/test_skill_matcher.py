from config.profile import candidate_profile
from job_matching.skill_matcher import find_skill_match


def main():
    job = {
        "job_title": "Azure Data Engineer",
        "description": (
            "Looking for an Azure Data Engineer with "
            "SQL, Python, Azure Data Factory, "
            "Databricks and PySpark experience."
        ),
    }

    result = find_skill_match(
        job,
        candidate_profile.core_skills,
        candidate_profile.additional_skills,
    )

    print("Matched Skills:")
    for skill in result["matched_skills"]:
        print(f"  - {skill}")

    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print(f"  - {skill}")


if __name__ == "__main__":
    main()