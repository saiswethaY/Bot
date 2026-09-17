from application.application_loader import create_application_records
from database.connection import get_connection


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT profile_id
                FROM candidate_profile
                ORDER BY profile_id DESC
                LIMIT 1;
                """
            )

            row = cursor.fetchone()

    if row is None:
        raise ValueError("No candidate profile found.")

    profile_id = row[0]

    inserted_count = create_application_records(profile_id)

    print("=" * 50)
    print("APPLICATION RECORD TEST")
    print("=" * 50)
    print(f"Profile ID       : {profile_id}")
    print(f"Records inserted : {inserted_count}")
    print("=" * 50)


if __name__ == "__main__":
    main()