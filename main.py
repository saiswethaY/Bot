from config.profile import candidate_profile
from config.settings import bot_settings


def main():
    print("=" * 50)
    print("JOB AUTO APPLICATOR")
    print("=" * 50)

    print(f"Environment      : {bot_settings.app_env}")
    print(f"LinkedIn Enabled  : {bot_settings.linkedin_enabled}")
    print(f"Naukri Enabled    : {bot_settings.naukri_enabled}")
    print(f"Minimum Match     : {bot_settings.minimum_match_score}%")
    print(
        f"Daily Application : "
        f"{bot_settings.max_applications_per_day}"
    )

    print("\nTarget Roles:")
    for role in candidate_profile.target_roles:
        print(f"  - {role}")

    print("\nCore Skills:")
    for skill in candidate_profile.core_skills:
        print(f"  - {skill}")

    print("\nPreferred Locations:")
    for location in candidate_profile.preferred_locations:
        print(f"  - {location}")

    print(
        f"\nExperience: "
        f"{candidate_profile.experience_min}"
        f"-"
        f"{candidate_profile.experience_max} years"
    )

    print(
        f"Notice Period: "
        f"{candidate_profile.notice_period_days} days"
    )

    print("\nConfiguration loaded successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()
