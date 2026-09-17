from config.settings import bot_settings


def make_application_decision(match_score: float) -> str:
    if match_score >= bot_settings.minimum_match_score:
        return "APPLY"

    return "SKIP"