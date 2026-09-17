from job_discovery.linkedin import LinkedInSource
from job_discovery.normalizer import normalize_job
from job_discovery.job_loader import load_jobs


def main():
    source = LinkedInSource()

    raw_jobs = source.fetch_jobs()

    normalized_jobs = [
        normalize_job(job)
        for job in raw_jobs
    ]

    inserted_count = load_jobs(normalized_jobs)

    print(f"LinkedIn jobs discovered : {len(raw_jobs)}")
    print(f"LinkedIn jobs normalized : {len(normalized_jobs)}")
    print(f"LinkedIn jobs inserted   : {inserted_count}")


if __name__ == "__main__":
    main()