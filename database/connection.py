import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not configured.")

    return psycopg.connect(database_url)


def test_connection():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            result = cursor.fetchone()

    print("PostgreSQL connection successful.")
    print(f"Database version: {result[0]}")


if __name__ == "__main__":
    test_connection()