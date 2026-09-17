from datetime import datetime


def send_notification(
    title: str,
    message: str,
) -> None:

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("=" * 60)
    print("NOTIFICATION")
    print("=" * 60)
    print(f"Time    : {timestamp}")
    print(f"Title   : {title}")
    print(f"Message : {message}")
    print("=" * 60)