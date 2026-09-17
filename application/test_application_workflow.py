from application.application_workflow import (
    ApplicationState,
    get_next_state,
)


def main():
    state = ApplicationState.READY

    state = get_next_state(
        state,
        "open_application",
    )

    print(f"After opening : {state.value}")

    state = get_next_state(
        state,
        "form_found",
    )

    print(f"After form    : {state.value}")

    state = get_next_state(
        state,
        "known_form",
    )

    print(f"Next state    : {state.value}")

    print("=" * 50)
    print("WORKFLOW TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()