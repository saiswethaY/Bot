def normalize_job(job: dict) -> dict:

    required_fields = [
        "source",
        "external_job_id",
        "job_title",
        "job_url",
    ]

    for field in required_fields:
        value = job.get(field)

        if value is None or not str(value).strip():
            raise ValueError(
                f"Required job field is missing: {field}"
            )

    description = str(
        job.get("description", "")
    ).strip()

    key_skills = str(
        job.get("key_skills", "")
    ).strip()

    if key_skills:
        description = (
            f"{description}\n"
            f"Key Skills: {key_skills}"
        ).strip()

    return {
        "source": str(
            job["source"]
        ).strip(),

        "external_job_id": str(
            job["external_job_id"]
        ).strip(),

        "job_title": str(
            job["job_title"]
        ).strip(),

        "company_name": str(
            job.get("company_name", "")
        ).strip(),

        "location": str(
            job.get("location", "")
        ).strip(),

        "experience_min": job.get(
            "experience_min"
        ),

        "experience_max": job.get(
            "experience_max"
        ),

        "job_url": str(
            job["job_url"]
        ).strip(),

        "description": description,
    }