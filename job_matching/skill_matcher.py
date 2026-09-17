import re


SKILL_ALIASES = {
    "sql": [
        "sql",
        "sparksql",
        "spark sql",
        "sql server",
        "mssql",
        "microsoft sql server",
    ],
    "python": [
        "python",
    ],
    "azure data factory": [
        "azure data factory",
        "azuredatafactory",
        "adf",
    ],
    "azure databricks": [
        "azure databricks",
        "azuredatabricks",
        "databricks",
        "data bricks",
        "databricks spark",
    ],
    "pyspark": [
        "pyspark",
        "py spark",
    ],
    "snowflake": [
        "snowflake",
    ],
    "adls gen2": [
        "adls gen2",
        "adls",
        "azure data lake",
        "azure data lake storage",
        "azure data lake storage gen2",
    ],
    "azure synapse analytics": [
        "azure synapse analytics",
        "azure synapse",
        "synapse analytics",
        "synapse",
    ],
    "delta lake": [
        "delta lake",
        "delta",
    ],
    "aws s3": [
        "aws s3",
        "amazon s3",
        "s3",
    ],
    "postgresql": [
        "postgresql",
        "postgres",
    ],
    "azure devops": [
        "azure devops",
        "azuredevops",
    ],
}


def normalize_text(value: str) -> str:
    text = str(value or "").lower()

    text = re.sub(
        r"[^a-z0-9+#]+",
        " ",
        text,
    )

    return " ".join(text.split())


def compact_text(value: str) -> str:
    return re.sub(
        r"[^a-z0-9+#]",
        "",
        str(value or "").lower(),
    )


def skill_matches(
    candidate_skill: str,
    job_text: str,
) -> bool:

    aliases = SKILL_ALIASES.get(
        candidate_skill.lower().strip(),
        [candidate_skill],
    )

    normal_text = normalize_text(job_text)
    compact_job = compact_text(job_text)

    for alias in aliases:

        normal_alias = normalize_text(alias)
        compact_alias = compact_text(alias)

        if normal_alias and normal_alias in normal_text:
            return True

        if compact_alias and compact_alias in compact_job:
            return True

    return False


def find_skill_match(
    job: dict,
    core_skills: list[str],
    additional_skills: list[str],
) -> dict:

    job_text = " ".join(
        [
            str(job.get("job_title", "")),
            str(job.get("company_name", "")),
            str(job.get("location", "")),
            str(job.get("description", "")),
            str(job.get("skills", "")),
            str(job.get("key_skills", "")),
            str(job.get("tags", "")),
        ]
    )

    core_matched = [
        skill
        for skill in core_skills
        if skill_matches(
            skill,
            job_text,
        )
    ]

    additional_matched = [
        skill
        for skill in additional_skills
        if skill_matches(
            skill,
            job_text,
        )
    ]

    matched = (
        core_matched
        + additional_matched
    )

    missing = [
        skill
        for skill in (
            core_skills
            + additional_skills
        )
        if skill not in matched
    ]

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "core_matched": core_matched,
        "additional_matched": additional_matched,
    }