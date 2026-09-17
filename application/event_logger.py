from database.connection import get_connection


def log_application_event(
    application_id: int,
    event_type: str,
    event_message: str,
) -> None:

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO application_events (
                    application_id,
                    event_type,
                    event_message
                )
                VALUES (%s, %s, %s);
                """,
                (
                    application_id,
                    event_type,
                    event_message,
                ),
            )