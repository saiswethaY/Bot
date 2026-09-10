from dataclasses import dataclass


@dataclass
class BotSettings:
    # Job matching
    minimum_match_score: int = 70

    # Application control
    max_applications_per_day: int = 10

    # Search control
    max_jobs_per_search: int = 50

    # Browser
    headless_browser: bool = False

    # Manual intervention
    pause_on_captcha: bool = True
    pause_on_otp: bool = True
    pause_on_unknown_form: bool = True

    # Duplicate handling
    skip_already_processed_jobs: bool = True


bot_settings = BotSettings()
