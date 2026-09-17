VALID_TRANSITIONS = {
    "READY": {
        "IN_PROGRESS",
    },

    "IN_PROGRESS": {
        "PAUSED",
        "FAILED",
        "SUBMITTED",
    },

    "PAUSED": {
        "IN_PROGRESS",
        "FAILED",
    },

    "FAILED": set(),

    "SUBMITTED": set(),
}


def validate_status_transition(
    current_status: str,
    new_status: str,
) -> None:

    if current_status not in VALID_TRANSITIONS:
        raise ValueError(
            f"Unknown current status: {current_status}"
        )

    allowed_statuses = VALID_TRANSITIONS[
        current_status
    ]

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Invalid status transition: "
            f"{current_status} -> {new_status}"
        )