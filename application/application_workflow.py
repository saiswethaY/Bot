from enum import Enum


class ApplicationState(Enum):
    READY = "READY"
    OPENING = "OPENING"
    FORM_DETECTED = "FORM_DETECTED"
    PAUSED_CAPTCHA = "PAUSED_CAPTCHA"
    PAUSED_OTP = "PAUSED_OTP"
    PAUSED_UNKNOWN_FORM = "PAUSED_UNKNOWN_FORM"
    READY_FOR_SUBMISSION = "READY_FOR_SUBMISSION"
    SUBMITTED = "SUBMITTED"
    FAILED = "FAILED"


def get_next_state(
    current_state: ApplicationState,
    event: str,
) -> ApplicationState:

    transitions = {
        (
            ApplicationState.READY,
            "open_application",
        ): ApplicationState.OPENING,

        (
            ApplicationState.OPENING,
            "form_found",
        ): ApplicationState.FORM_DETECTED,

        (
            ApplicationState.FORM_DETECTED,
            "known_form",
        ): ApplicationState.READY_FOR_SUBMISSION,

        (
            ApplicationState.FORM_DETECTED,
            "captcha_detected",
        ): ApplicationState.PAUSED_CAPTCHA,

        (
            ApplicationState.FORM_DETECTED,
            "otp_required",
        ): ApplicationState.PAUSED_OTP,

        (
            ApplicationState.FORM_DETECTED,
            "unknown_form",
        ): ApplicationState.PAUSED_UNKNOWN_FORM,

        (
            ApplicationState.READY_FOR_SUBMISSION,
            "submission_success",
        ): ApplicationState.SUBMITTED,

        (
            ApplicationState.READY_FOR_SUBMISSION,
            "submission_failed",
        ): ApplicationState.FAILED,
    }

    next_state = transitions.get(
        (current_state, event)
    )

    if next_state is None:
        raise ValueError(
            f"Invalid transition: "
            f"{current_state.value} -> {event}"
        )

    return next_state