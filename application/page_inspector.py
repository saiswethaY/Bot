from playwright.sync_api import Page


def get_page_text(page: Page) -> str:
    try:
        return page.locator("body").inner_text().lower()
    except Exception:
        return ""


def inspect_page(page: Page) -> str:
    url = page.url.lower()
    title = page.title().lower()
    content = get_page_text(page)

    # ---------------------------------------------------------
    # SECURITY / AUTHENTICATION STATES
    # ---------------------------------------------------------

    captcha_indicators = [
        "captcha",
        "verify you are human",
        "i'm not a robot",
        "security verification",
    ]

    if any(
        indicator in content or indicator in url
        for indicator in captcha_indicators
    ):
        return "CAPTCHA"

    otp_indicators = [
        "otp",
        "one-time password",
        "verification code",
        "enter verification code",
    ]

    if any(
        indicator in content
        for indicator in otp_indicators
    ):
        return "OTP"

    login_indicators = [
        "login",
        "log in",
        "sign in",
        "sign-in",
        "register / login",
    ]

    # Only classify as login when the page strongly indicates
    # that authentication is actually required.
    login_form_indicators = [
        "enter your email",
        "enter your mobile",
        "enter mobile number",
        "enter password",
        "forgot password",
        "login to apply",
    ]

    has_login_form = any(
        indicator in content
        for indicator in login_form_indicators
    )

    has_login_text = any(
        indicator in content
        for indicator in login_indicators
    )

    if has_login_form or (
        has_login_text
        and not _looks_like_authenticated_naukri_page(content)
    ):
        return "LOGIN_REQUIRED"

    # ---------------------------------------------------------
    # APPLICATION FORM
    # ---------------------------------------------------------

    if _looks_like_application_form(page, content):
        return "APPLICATION_FORM"

    # ---------------------------------------------------------
    # Naukri JOB PAGE
    # ---------------------------------------------------------

    if _looks_like_job_page(page, url, title, content):
        return "JOB_PAGE"

    # ---------------------------------------------------------
    # TEST PAGE
    # ---------------------------------------------------------

    if "example domain" in title:
        return "TEST_PAGE"

    # ---------------------------------------------------------
    # UNKNOWN
    # ---------------------------------------------------------

    return "UNKNOWN"


def _looks_like_authenticated_naukri_page(
    content: str,
) -> bool:

    authenticated_indicators = [
        "my naukri",
        "profile",
        "applications",
        "jobs you may like",
        "recommended jobs",
        "job alerts",
    ]

    return any(
        indicator in content
        for indicator in authenticated_indicators
    )


def _looks_like_application_form(
    page: Page,
    content: str,
) -> bool:

    form_count = page.locator("form").count()

    application_indicators = [
        "apply for this job",
        "application form",
        "resume",
        "upload resume",
        "cover letter",
        "work experience",
        "current ctc",
        "expected ctc",
        "notice period",
    ]

    indicator_count = sum(
        1
        for indicator in application_indicators
        if indicator in content
    )

    # A form by itself is not enough.
    # Require application-specific content.
    if form_count > 0 and indicator_count >= 1:
        return True

    return indicator_count >= 2


def _looks_like_job_page(
    page: Page,
    url: str,
    title: str,
    content: str,
) -> bool:

    naukri_url = (
        "naukri.com/job-listings" in url
        or "naukri.com/" in url
    )

    job_indicators = [
        "job description",
        "key skills",
        "experience",
        "salary",
        "education",
        "about company",
        "apply",
    ]

    indicator_count = sum(
        1
        for indicator in job_indicators
        if indicator in content
    )

    return (
        naukri_url
        and indicator_count >= 2
    )


def print_page_inspection(page: Page) -> None:

    page_type = inspect_page(page)

    print("=" * 60)
    print("PAGE INSPECTION")
    print("=" * 60)
    print(f"URL        : {page.url}")
    print(f"Title      : {page.title()}")
    print(f"Page type  : {page_type}")
    print("=" * 60)