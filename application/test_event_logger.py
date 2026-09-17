from application.event_logger import log_application_event


def main():
    application_id = 1

    log_application_event(
        application_id=application_id,
        event_type="TEST_EVENT",
        event_message="Event logger test successful.",
    )

    print("=" * 50)
    print("EVENT LOGGER TEST")
    print("=" * 50)
    print(f"Application ID : {application_id}")
    print("Event logged   : TEST_EVENT")
    print("=" * 50)


if __name__ == "__main__":
    main()