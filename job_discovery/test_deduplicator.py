from job_discovery.deduplicator import deduplicate_jobs


def main():
    jobs = [
        {
            "job_title": "Azure Data Engineer",
            "company_name": "ABC Corp",
            "location": "Bangalore",
        },
        {
            "job_title": " azure   data engineer ",
            "company_name": "abc corp",
            "location": " BANGALORE ",
        },
        {
            "job_title": "Azure Data Engineer",
            "company_name": "XYZ Corp",
            "location": "Bangalore",
        },
        {
            "job_title": "Python Developer",
            "company_name": "ABC Corp",
            "location": "Bangalore",
        },
    ]

    unique_jobs = deduplicate_jobs(jobs)

    print(f"Input jobs  : {len(jobs)}")
    print(f"Unique jobs : {len(unique_jobs)}")

    print("\nRemaining jobs:")

    for job in unique_jobs:
        print(
            f"- {job['job_title']} | "
            f"{job['company_name']} | "
            f"{job['location']}"
        )


if __name__ == "__main__":
    main()