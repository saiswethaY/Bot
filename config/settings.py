import os

from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class BotSettings:
    app_env: str = os.getenv("APP_ENV", "development")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://localhost:5432/job_applicator",
    )

    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    linkedin_enabled: bool = (
        os.getenv("LINKEDIN_ENABLED", "true").lower() == "true"
    )

    naukri_enabled: bool = (
        os.getenv("NAUKRI_ENABLED", "true").lower() == "true"
    )

    minimum_match_score: int = 70

    max_applications_per_day: int = 10

    max_jobs_per_search: int = 50

    headless_browser: bool = False

    pause_on_captcha: bool = True

    pause_on_otp: bool = True

    pause_on_unknown_form: bool = True

    skip_already_processed_jobs: bool = True


bot_settings = BotSettings()
