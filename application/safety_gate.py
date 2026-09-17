from application.page_inspector import inspect_page


PAUSE_PAGE_TYPES = {
    "CAPTCHA",
    "OTP",
    "LOGIN_REQUIRED",
    "UNKNOWN",
}

CONTINUE_PAGE_TYPES = {
    "JOB_PAGE",
    "APPLICATION_FORM",
}


def check_page_safety(page) -> str:

    page_type = inspect_page(page)

    if page_type in PAUSE_PAGE_TYPES:
        return "PAUSE"

    if page_type in CONTINUE_PAGE_TYPES:
        return "CONTINUE"

    return "STOP"