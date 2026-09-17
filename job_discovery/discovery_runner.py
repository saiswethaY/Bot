from config.settings import bot_settings

from job_discovery.linkedin import LinkedInSource
from job_discovery.naukri import NaukriSource
from job_discovery.normalizer import normalize_job
from job_discovery.deduplicator import deduplicate_jobs
from job_discovery.job_loader import load_jobs


def run_discovery():
    all_jobs = []

    if bot_settings.linkedin_enabled:
        linkedin_source = LinkedInSource()
        linkedin_jobs = linkedin_source.fetch_jobs()
        all_jobs.extend(linkedin_jobs)

    if bot_settings.naukri_enabled:
        naukri_source = NaukriSource()
        naukri_jobs = naukri_source.fetch_jobs()
        all_jobs.extend(naukri_jobs)

    normalized_jobs = [
        normalize_job(job)
        for job in all_jobs
    ]

    unique_jobs = deduplicate_jobs(normalized_jobs)

    inserted_count = load_jobs(unique_jobs)

    print("=" * 50)
    print("JOB DISCOVERY RUN")
    print("=" * 50)

    print(f"Jobs discovered : {len(all_jobs)}")
    print(f"Jobs normalized : {len(normalized_jobs)}")
    print(f"Unique jobs     : {len(unique_jobs)}")
    print(f"Jobs inserted   : {inserted_count}")

    print("=" * 50)


if __name__ == "__main__":
    run_discovery()