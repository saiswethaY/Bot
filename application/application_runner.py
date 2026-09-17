import sys

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from application.application_workflow import ApplicationState
from application.browser_manager import BrowserManager
from application.event_logger import log_application_event
from application.job_url_resolver import get_job_url
from application.page_inspector import inspect_page
from application.safety_gate import check_page_safety
from application.workflow_controller import start_application_workflow
from database.connection import get_connection


def get_application_status(application_id: int) -> str | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT application_status
                FROM applications
                WHERE application_id = %s;
                """,
                (application_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return row[0]


def find_apply_button(page):
    selectors = [
        "button:has-text('Apply')",
        "a:has-text('Apply')",
        "button:has-text('Apply on company site')",
        "a:has-text('Apply on company site')",
        "[class*='apply']",
    ]

    for selector in selectors:
        try:
            locator = page.locator(selector)
            count = locator.count()

            for index in range(count):
                button = locator.nth(index)

                if not button.is_visible():
                    continue

                text = button.inner_text().strip().lower()

                if "apply" in text:
                    return button

        except Exception:
            continue

    return None


def click_apply_button(page, application_id: int) -> bool:
    print("Searching for Apply button...")

    button = find_apply_button(page)

    if button is None:
        log_application_event(
            application_id,
            "APPLY_BUTTON_NOT_FOUND",
            "Could not identify a visible Apply button.",
        )

        print("Apply button not found.")

        return False

    try:
        button.scroll_into_view_if_needed()

        button_text = button.inner_text().strip()

        print(f"Apply button found: {button_text}")

        button.click()

        page.wait_for_timeout(3000)

        log_application_event(
            application_id,
            "APPLY_BUTTON_CLICKED",
            "Apply button was clicked.",
        )

        print("Apply button clicked.")

        return True

    except Exception as error:

        log_application_event(
            application_id,
            "APPLY_BUTTON_FAILED",
            f"Failed to click Apply button: {error}",
        )

        print(
            f"Failed to click Apply button: {error}"
        )

        return False


def wait_for_manual_login(page, application_id: int) -> bool:

    print()
    print("=" * 60)
    print("NAUKRI LOGIN REQUIRED")
    print("=" * 60)
    print("Complete the login manually in the browser.")
    print("If Naukri asks for OTP or CAPTCHA, complete it manually.")
    print("Do not bypass any security verification.")
    print("=" * 60)

    input(
        "Press ENTER after completing the manual action..."
    )

    page.wait_for_timeout(2000)

    page_type = inspect_page(page)

    print(
        f"Page after manual action: {page_type}"
    )

    log_application_event(
        application_id,
        "MANUAL_ACTION_RECHECK",
        f"Page type after manual action: {page_type}",
    )

    if page_type in {
        "LOGIN_REQUIRED",
        "CAPTCHA",
        "OTP",
    }:
        print()
        print(
            f"Manual action still required: {page_type}"
        )

        return False

    if page_type == "UNKNOWN":
        print()
        print(
            "Page is still UNKNOWN."
        )

        return False

    return True


def handle_security_state(
    page,
    application_id: int,
    page_type: str,
) -> str:

    if page_type not in {
        "LOGIN_REQUIRED",
        "CAPTCHA",
        "OTP",
    }:
        return page_type

    print()
    print("=" * 60)
    print("MANUAL INTERVENTION REQUIRED")
    print("=" * 60)
    print(f"Detected page : {page_type}")
    print("The bot will not bypass this protection.")
    print("Complete the required action manually.")
    print("=" * 60)

    input(
        "Press ENTER after completing the manual action..."
    )

    page.wait_for_timeout(2000)

    new_page_type = inspect_page(page)

    print(
        f"Page after manual action: {new_page_type}"
    )

    log_application_event(
        application_id,
        "SECURITY_RECHECK",
        (
            f"Before: {page_type}; "
            f"After: {new_page_type}"
        ),
    )

    return new_page_type


def inspect_application_form(
    page,
    application_id: int,
) -> str:

    page_type = inspect_page(page)

    log_application_event(
        application_id,
        "APPLICATION_PAGE_INSPECTED",
        f"Detected page type: {page_type}",
    )

    return page_type


def fill_text_field(
    page,
    labels: list[str],
    value: str,
) -> bool:

    if not value:
        return False

    for label in labels:

        try:
            locator = page.get_by_label(
                label,
                exact=False,
            )

            if locator.count() == 0:
                continue

            field = locator.first

            if not field.is_visible():
                continue

            field.fill(value)

            return True

        except Exception:
            continue

    return False


def fill_common_fields(
    page,
    application_id: int,
) -> int:

    filled_count = 0

    fields = [
        (
            ["First Name", "First name"],
            "SaiSwetha",
        ),
        (
            ["Last Name", "Last name"],
            "Yendluri",
        ),
        (
            ["Full Name", "Full name"],
            "SaiSwetha Yendluri",
        ),
        (
            ["Email", "Email Address"],
            "saiswethayendluri@gmail.com",
        ),
    ]

    for labels, value in fields:

        if fill_text_field(
            page,
            labels,
            value,
        ):

            filled_count += 1

            log_application_event(
                application_id,
                "FIELD_FILLED",
                f"Filled application field: {labels[0]}",
            )

            print(
                f"Field filled     : {labels[0]}"
            )

    return filled_count


def detect_resume_upload(page):

    selectors = [
        "input[type='file']",
        "input[accept*='pdf']",
        "input[accept*='document']",
    ]

    for selector in selectors:

        try:
            locator = page.locator(selector)

            if locator.count() > 0:
                return locator.first

        except Exception:
            continue

    return None


def prepare_resume_upload(
    page,
    application_id: int,
) -> bool:

    upload_field = detect_resume_upload(page)

    if upload_field is None:

        log_application_event(
            application_id,
            "RESUME_UPLOAD_NOT_FOUND",
            "No recognizable resume upload field was found.",
        )

        print(
            "Resume upload field not found."
        )

        return False

    log_application_event(
        application_id,
        "RESUME_UPLOAD_READY",
        "Resume upload field detected.",
    )

    print(
        "Resume upload field detected."
    )

    return True


def wait_for_manual_review(
    application_id: int,
) -> None:

    log_application_event(
        application_id,
        "MANUAL_REVIEW_REQUIRED",
        "Application is ready for final manual review.",
    )

    print()
    print("=" * 60)
    print("MANUAL REVIEW REQUIRED")
    print("=" * 60)
    print("The application has been prepared.")
    print("Review all information in the browser.")
    print("The bot will NOT click the final Submit button.")
    print("Final submission requires your confirmation.")
    print("=" * 60)

    input(
        "Press ENTER after reviewing the application..."
    )


def run_application_workflow(
    application_id: int,
) -> None:

    # ---------------------------------------------------------
    # DATABASE STATUS CHECK
    # ---------------------------------------------------------

    application_status = get_application_status(
        application_id
    )

    if application_status is None:
        raise ValueError(
            f"Application {application_id} was not found."
        )

    if application_status == "SUBMITTED":
        print("=" * 60)
        print("APPLICATION ALREADY SUBMITTED")
        print("=" * 60)
        print(
            f"Application ID : {application_id}"
        )
        print(
            "The bot will not open the job again."
        )
        print("=" * 60)

        return

    if application_status != "READY":
        print("=" * 60)
        print("APPLICATION NOT READY")
        print("=" * 60)
        print(
            f"Application ID : {application_id}"
        )
        print(
            f"Current status : {application_status}"
        )
        print("=" * 60)

        return

    # ---------------------------------------------------------
    # START WORKFLOW
    # ---------------------------------------------------------

    current_state = start_application_workflow(
        application_id
    )

    log_application_event(
        application_id,
        "WORKFLOW_STARTED",
        f"Workflow started in state: {current_state.value}",
    )

    print("=" * 60)
    print("REAL APPLICATION WORKFLOW")
    print("=" * 60)
    print(
        f"Application ID : {application_id}"
    )
    print(
        f"Initial state  : {current_state.value}"
    )

    job_url = get_job_url(
        application_id
    )

    print(
        f"Job URL        : {job_url}"
    )

    with sync_playwright() as playwright:

        browser_manager = BrowserManager(
            playwright
        )

        try:

            # -------------------------------------------------
            # OPEN BROWSER
            # -------------------------------------------------

            current_state = ApplicationState.OPENING

            log_application_event(
                application_id,
                "BROWSER_OPENING",
                "Opening persistent browser.",
            )

            print(
                f"State          : {current_state.value}"
            )

            page = browser_manager.start()

            page.goto(
                job_url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            page.wait_for_timeout(3000)

            log_application_event(
                application_id,
                "PAGE_OPENED",
                f"Opened job URL: {page.url}",
            )

            print(
                f"Current URL    : {page.url}"
            )

            # -------------------------------------------------
            # INSPECT PAGE
            # -------------------------------------------------

            page_type = inspect_page(page)

            print(
                f"Initial page   : {page_type}"
            )

            safety_decision = check_page_safety(
                page
            )

            print(
                f"Safety decision: {safety_decision}"
            )

            # -------------------------------------------------
            # SECURITY STATES
            # -------------------------------------------------

            if page_type in {
                "LOGIN_REQUIRED",
                "CAPTCHA",
                "OTP",
            }:

                page_type = handle_security_state(
                    page,
                    application_id,
                    page_type,
                )

                if page_type in {
                    "LOGIN_REQUIRED",
                    "CAPTCHA",
                    "OTP",
                }:

                    print()
                    print(
                        "Required manual action was not completed."
                    )

                    return

            # -------------------------------------------------
            # UNKNOWN
            # -------------------------------------------------

            if page_type == "UNKNOWN":

                log_application_event(
                    application_id,
                    "WORKFLOW_STOPPED",
                    "Page could not be recognized.",
                )

                print()
                print(
                    "Workflow stopped: page is UNKNOWN."
                )

                return

            # -------------------------------------------------
            # JOB PAGE
            # -------------------------------------------------

            if page_type == "JOB_PAGE":

                print()
                print(
                    "Naukri job page recognized."
                )

                print(
                    "Proceeding to Apply button."
                )

                apply_clicked = click_apply_button(
                    page,
                    application_id,
                )

                if not apply_clicked:

                    log_application_event(
                        application_id,
                        "WORKFLOW_STOPPED",
                        "Apply button unavailable.",
                    )

                    return

                page.wait_for_timeout(3000)

            # -------------------------------------------------
            # APPLICATION FORM
            # -------------------------------------------------

            after_apply_type = inspect_application_form(
                page,
                application_id,
            )

            print(
                f"After Apply    : {after_apply_type}"
            )

            # -------------------------------------------------
            # SECURITY AFTER APPLY
            # -------------------------------------------------

            if after_apply_type in {
                "LOGIN_REQUIRED",
                "CAPTCHA",
                "OTP",
            }:

                after_apply_type = handle_security_state(
                    page,
                    application_id,
                    after_apply_type,
                )

                if after_apply_type in {
                    "LOGIN_REQUIRED",
                    "CAPTCHA",
                    "OTP",
                }:

                    print(
                        "Security verification still required."
                    )

                    return

            # -------------------------------------------------
            # UNKNOWN AFTER APPLY
            # -------------------------------------------------

            if after_apply_type == "UNKNOWN":

                log_application_event(
                    application_id,
                    "WORKFLOW_STOPPED",
                    "Application page could not be recognized.",
                )

                print(
                    "Application page is UNKNOWN."
                )

                return

            # -------------------------------------------------
            # FORM DETECTED
            # -------------------------------------------------

            if after_apply_type != "APPLICATION_FORM":

                log_application_event(
                    application_id,
                    "WORKFLOW_STOPPED",
                    (
                        "Expected application form but detected "
                        f"{after_apply_type}."
                    ),
                )

                print(
                    "Application form was not detected."
                )

                return

            current_state = ApplicationState.FORM_DETECTED

            log_application_event(
                application_id,
                "APPLICATION_FORM_DETECTED",
                "Application form detected.",
            )

            print(
                f"State          : {current_state.value}"
            )

            # -------------------------------------------------
            # FILL COMMON FIELDS
            # -------------------------------------------------

            filled_count = fill_common_fields(
                page,
                application_id,
            )

            print(
                f"Fields filled  : {filled_count}"
            )

            # -------------------------------------------------
            # RESUME
            # -------------------------------------------------

            resume_detected = prepare_resume_upload(
                page,
                application_id,
            )

            if resume_detected:
                print(
                    "Resume upload  : AVAILABLE"
                )
            else:
                print(
                    "Resume upload  : NOT FOUND"
                )

            # -------------------------------------------------
            # MANUAL REVIEW
            # -------------------------------------------------

            current_state = (
                ApplicationState.READY_FOR_SUBMISSION
            )

            log_application_event(
                application_id,
                "READY_FOR_SUBMISSION",
                (
                    "Application prepared and waiting "
                    "for final manual review."
                ),
            )

            print()
            print(
                f"State          : {current_state.value}"
            )

            wait_for_manual_review(
                application_id
            )

        except PlaywrightTimeoutError as error:

            log_application_event(
                application_id,
                "WORKFLOW_FAILED",
                f"Browser timeout: {error}",
            )

            print()
            print(
                f"Browser timeout: {error}"
            )

        except Exception as error:

            log_application_event(
                application_id,
                "WORKFLOW_FAILED",
                f"Unexpected workflow error: {error}",
            )

            print()
            print(
                f"Workflow error: {error}"
            )

        finally:

            browser_manager.close()

            log_application_event(
                application_id,
                "BROWSER_CLOSED",
                "Browser closed after workflow.",
            )

    print("=" * 60)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: "
            "python -m application.application_runner "
            "<application_id>"
        )

    try:
        application_id = int(sys.argv[1])

    except ValueError:
        raise SystemExit(
            "Application ID must be a number."
        )

    run_application_workflow(
        application_id
    )