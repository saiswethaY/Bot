def _normalize_text(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


def get_job_key(job: dict) -> tuple[str, str, str]:
    return (
        _normalize_text(job.get("job_title")),
        _normalize_text(job.get("company_name")),
        _normalize_text(job.get("location")),
    )


def deduplicate_jobs(jobs: list[dict]) -> list[dict]:
    unique_jobs = []
    seen_keys = set()

    for job in jobs:
        job_key = get_job_key(job)

        if job_key in seen_keys:
            continue

        seen_keys.add(job_key)
        unique_jobs.append(job)

    return unique_jobs