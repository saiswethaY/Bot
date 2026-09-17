from job_discovery.normalizer import normalize_job


def main():
    valid_job = {
        "source": "TEST",
        "external_job_id": "TEST-003",
        "job_title": "Azure Data Engineer",
        "company_name": "Demo Company",
        "location": "Bangalore",
        "experience_min": 2.0,
        "experience_max": 4.0,
        "job_url": "https://example.com/jobs/TEST-003",
        "description": "SQL, Python and Databricks",
    }

    invalid_job = {
        "source": "TEST",
        "external_job_id": "TEST-004",
        "job_title": "",
        "company_name": "Demo Company",
        "location": "Bangalore",
        "experience_min": 2.0,
        "experience_max": 4.0,
        "job_url": "https://example.com/jobs/TEST-004",
        "description": "SQL and Python",
    }

    print("Testing valid job...")

    normalized_job = normalize_job(valid_job)

    print("Valid job accepted.")
    print(normalized_job)

    print("\nTesting invalid job...")

    try:
        normalize_job(invalid_job)
        print("ERROR: Invalid job was accepted.")
    except ValueError as error:
        print(f"Invalid job rejected: {error}")


if __name__ == "__main__":
    main()