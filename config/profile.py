from dataclasses import dataclass, field


@dataclass
class CandidateProfile:
    target_roles: list[str] = field(default_factory=list)
    core_skills: list[str] = field(default_factory=list)
    additional_skills: list[str] = field(default_factory=list)
    preferred_locations: list[str] = field(default_factory=list)

    experience_min: float = 0.0
    experience_max: float = 0.0

    work_modes: list[str] = field(default_factory=list)

    notice_period_days: int = 0


candidate_profile = CandidateProfile(
    target_roles=[
        "Data Engineer",
        "Associate Data Engineer",
        "Azure Data Engineer",
        "Databricks Engineer",
        "Data Engineer Developer",
    ],

    core_skills=[
        "SQL",
        "Python",
        "Azure Data Factory",
        "Azure Databricks",
        "PySpark",
        "Snowflake",
        "ADLS Gen2",
    ],

    additional_skills=[
        "Azure Synapse Analytics",
        "Delta Lake",
        "AWS S3",
        "PostgreSQL",
        "Microsoft SQL Server",
        "Azure DevOps",
    ],

    preferred_locations=[
        "Bangalore",
        "Hyderabad",
        "Pune",
        "Chennai",
        "Remote",
    ],

    experience_min=2.0,
    experience_max=3.0,

    work_modes=[
        "Remote",
        "Hybrid",
        "On-site",
    ],

    notice_period_days=30,
)
