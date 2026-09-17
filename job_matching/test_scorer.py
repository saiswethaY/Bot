from job_matching.scorer import calculate_match_score


def main():
    job = {
        "job_title": "Azure Data Engineer",
        "company_name": "Demo Analytics",
        "location": "Bangalore",
        "experience_min": 2.0,
        "experience_max": 4.0,
        "description": (
            "Looking for an Azure Data Engineer with "
            "SQL, Python, Azure Data Factory, "
            "Azure Databricks and PySpark experience."
        ),
    }

    result = calculate_match_score(job)

    print("=" * 50)
    print("JOB MATCH RESULT")
    print("=" * 50)

    print(f"Match Score      : {result['match_score']}%")
    print(f"Role Match       : {result['role_match']}")
    print(f"Location Match   : {result['location_match']}")
    print(f"Experience Match : {result['experience_match']}")

    print("\nMatched Skills:")
    for skill in result["matched_skills"]:
        print(f"  - {skill}")

    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print(f"  - {skill}")

    print("=" * 50)


if __name__ == "__main__":
    main()