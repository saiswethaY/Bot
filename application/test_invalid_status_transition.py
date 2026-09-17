from application.application_tracker import (
    update_application_status,
)


def main():
    application_id = 1

    try:
        update_application_status(
            application_id,
            "SUBMITTED",
        )

        print("ERROR: Invalid transition was allowed.")

    except ValueError as error:
        print("=" * 50)
        print("INVALID TRANSITION TEST")
        print("=" * 50)
        print("Invalid transition correctly rejected.")
        print(f"Reason: {error}")
        print("=" * 50)


if __name__ == "__main__":
    main()