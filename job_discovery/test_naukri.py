from job_discovery.naukri import NaukriSource


def main():
    source = NaukriSource()

    jobs = source.fetch_jobs()

    print(f"Naukri jobs discovered: {len(jobs)}")

    for job in jobs:
        print("-" * 40)
        print(f"Source   : {job['source']}")
        print(f"Job ID   : {job['external_job_id']}")
        print(f"Title    : {job['job_title']}")
        print(f"Company  : {job['company_name']}")
        print(f"Location : {job['location']}")


if __name__ == "__main__":
    main()