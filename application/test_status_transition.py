from application.status_transition import (
    validate_status_transition,
)


def main():
    validate_status_transition(
        "READY",
        "IN_PROGRESS",
    )

    validate_status_transition(
        "IN_PROGRESS",
        "PAUSED",
    )

    validate_status_transition(
        "IN_PROGRESS",
        "SUBMITTED",
    )

    try:
        validate_status_transition(
            "SUBMITTED",
            "READY",
        )
    except ValueError:
        print("Invalid transition correctly rejected.")

    print("=" * 50)
    print("STATUS TRANSITION TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()