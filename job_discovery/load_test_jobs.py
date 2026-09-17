from job_discovery.job_loader import load_jobs
from job_discovery.normalizer import normalize_job
from job_discovery.test_source import TestJobSource


def main():
    source = TestJobSource()

    raw_jobs = source.fetch_jobs()

    normalized_jobs = [
        normalize_job(job)
        for job in raw_jobs
    ]

    inserted_count = load_jobs(normalized_jobs)

    print(f"Jobs discovered  : {len(raw_jobs)}")
    print(f"Jobs normalized  : {len(normalized_jobs)}")
    print(f"Jobs inserted    : {inserted_count}")


if __name__ == "__main__":
    main()