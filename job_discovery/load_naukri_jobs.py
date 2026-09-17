from job_discovery.naukri import NaukriSource
from job_discovery.normalizer import normalize_job
from job_discovery.job_loader import load_jobs


def main():
    source = NaukriSource()

    raw_jobs = source.fetch_jobs()

    normalized_jobs = [
        normalize_job(job)
        for job in raw_jobs
    ]

    inserted_count = load_jobs(normalized_jobs)

    print(f"Naukri jobs discovered : {len(raw_jobs)}")
    print(f"Naukri jobs normalized : {len(normalized_jobs)}")
    print(f"Naukri jobs inserted   : {inserted_count}")


if __name__ == "__main__":
    main()