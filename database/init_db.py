from pathlib import Path

from database.connection import get_connection


def initialize_database():
    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    statements = [
        statement.strip()
        for statement in schema.split(";")
        if statement.strip()
    ]

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        connection.commit()
        print("Database schema initialized successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Database initialization failed: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()