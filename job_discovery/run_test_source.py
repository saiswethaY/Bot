from job_discovery.test_source import TestJobSource


def main():
    source = TestJobSource()

    jobs = source.fetch_jobs()

    print(f"Jobs discovered: {len(jobs)}")

    for job in jobs:
        print("-" * 40)
        print(f"Title    : {job['job_title']}")
        print(f"Company  : {job['company_name']}")
        print(f"Location : {job['location']}")
        print(f"Source   : {job['source']}")


if __name__ == "__main__":
    main()