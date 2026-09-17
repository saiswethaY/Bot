from pathlib import Path
from urllib.parse import quote
from datetime import datetime, timedelta
import re

from playwright.sync_api import sync_playwright

from config.profile import candidate_profile
from job_discovery.base import JobSource


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

SESSION_DIR = Path(".browser_session/naukri")

MAX_FRESHNESS_DAYS = 7


class NaukriSource(JobSource):

    BASE_URL = "https://www.naukri.com"

    # ---------------------------------------------------------
    # SEARCH URL
    # ---------------------------------------------------------

    def _build_search_url(
        self,
        role: str,
        location: str,
    ) -> str:

        role_part = quote(
            role.lower().replace(" ", "-")
        )

        location_part = quote(
            location.lower().replace(" ", "-")
        )

        return (
            f"{self.BASE_URL}/"
            f"{role_part}-jobs-in-{location_part}"
        )

    # ---------------------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------------------

    def _extract_experience(
        self,
        job_url: str,
    ) -> tuple[float | None, float | None]:

        if not job_url:
            return None, None

        match = re.search(
            r"(\d+(?:\.\d+)?)-to-(\d+(?:\.\d+)?)-years",
            job_url.lower(),
        )

        if not match:
            return None, None

        return (
            float(match.group(1)),
            float(match.group(2)),
        )

    # ---------------------------------------------------------
    # POSTED DATE
    # ---------------------------------------------------------

    def _extract_posted_at(
        self,
        text: str,
    ):

        if not text:
            return None

        text = text.lower().strip()

        # -----------------------------------------------------
        # FORMAT 1
        #
        # Examples:
        # 30 minutes ago
        # 5 hours ago
        # 1 day ago
        # 3 days ago
        # 1 week ago
        # 2 weeks ago
        # 1 month ago
        # -----------------------------------------------------

        match = re.search(
            r"(\d+)\s+"
            r"(minute|minutes|hour|hours|day|days|"
            r"week|weeks|month|months)\s+ago",
            text,
        )

        if match:

            value = int(match.group(1))
            unit = match.group(2)

            if "minute" in unit:

                delta = timedelta(
                    minutes=value
                )

            elif "hour" in unit:

                delta = timedelta(
                    hours=value
                )

            elif "day" in unit:

                delta = timedelta(
                    days=value
                )

            elif "week" in unit:

                delta = timedelta(
                    weeks=value
                )

            elif "month" in unit:

                delta = timedelta(
                    days=value * 30
                )

            else:

                return None

            return datetime.now() - delta

        # -----------------------------------------------------
        # FORMAT 2
        #
        # Naukri Recommended Jobs commonly uses:
        #
        # 5d ago
        # 3h ago
        # 30m ago
        # 1w ago
        # 2mo ago
        # -----------------------------------------------------

        compact_match = re.search(
            r"(\d+)\s*"
            r"(m|h|d|w|mo)\s+ago",
            text,
        )

        if compact_match:

            value = int(
                compact_match.group(1)
            )

            unit = compact_match.group(2)

            if unit == "m":

                delta = timedelta(
                    minutes=value
                )

            elif unit == "h":

                delta = timedelta(
                    hours=value
                )

            elif unit == "d":

                delta = timedelta(
                    days=value
                )

            elif unit == "w":

                delta = timedelta(
                    weeks=value
                )

            elif unit == "mo":

                delta = timedelta(
                    days=value * 30
                )

            else:

                return None

            return datetime.now() - delta

        # -----------------------------------------------------
        # TODAY
        # -----------------------------------------------------

        if "today" in text:

            return datetime.now()

        return None

    # ---------------------------------------------------------
    # FRESHNESS
    # ---------------------------------------------------------

    def _is_fresh(
        self,
        posted_at,
    ) -> bool:

        if posted_at is None:

            return False

        age = (
            datetime.now()
            - posted_at
        )

        return (
            age
            <= timedelta(
                days=MAX_FRESHNESS_DAYS
            )
        )

    # ---------------------------------------------------------
    # PAGE STATE
    # ---------------------------------------------------------

    def _get_page_state(
        self,
        page,
    ) -> str:

        current_url = (
            page.url.lower()
        )

        try:

            body_text = (
                page.locator("body")
                .inner_text()
                .lower()
            )

        except Exception:

            body_text = ""

        if "captcha" in body_text:

            return "CAPTCHA"

        if (
            "otp" in body_text
            or "one time password" in body_text
        ):

            return "OTP"

        if "login" in current_url:

            return "LOGIN_REQUIRED"

        return "READY"

    # ---------------------------------------------------------
    # KEY SKILLS
    # ---------------------------------------------------------

    def _extract_key_skills(
        self,
        card,
    ) -> str:

        selectors = [
            ".tags-gt",
            ".job-desc .tags-gt",
            ".row.tags-gt",
            "[class*='tags-gt']",
        ]

        for selector in selectors:

            try:

                elements = card.locator(
                    selector
                )

                if elements.count() > 0:

                    text = (
                        elements.first
                        .inner_text()
                        .strip()
                    )

                    if text:

                        return text

            except Exception:

                continue

        return ""

    # ---------------------------------------------------------
    # SEARCH JOBS
    # ---------------------------------------------------------

    def _extract_search_jobs(
        self,
        page,
    ) -> list[dict]:

        jobs = []

        cards = page.locator(
            "div.srp-jobtuple-wrapper"
        )

        card_count = cards.count()

        print(
            f"Search job cards detected : "
            f"{card_count}"
        )

        for index in range(
            card_count
        ):

            card = cards.nth(
                index
            )

            try:

                title = card.locator(
                    "a.title"
                )

                company = card.locator(
                    "a.comp-name"
                )

                location = card.locator(
                    ".locWdth"
                )

                description = card.locator(
                    ".job-desc"
                )

                job_title = (
                    title.inner_text().strip()
                    if title.count()
                    else ""
                )

                company_name = (
                    company.inner_text().strip()
                    if company.count()
                    else ""
                )

                job_location = (
                    location.inner_text().strip()
                    if location.count()
                    else ""
                )

                job_description = (
                    description
                    .inner_text()
                    .strip()
                    if description.count()
                    else ""
                )

                job_url = (
                    title.get_attribute(
                        "href"
                    )
                    if title.count()
                    else ""
                )

                if (
                    not job_title
                    or not job_url
                ):

                    continue

                (
                    experience_min,
                    experience_max,
                ) = self._extract_experience(
                    job_url
                )

                key_skills = (
                    self._extract_key_skills(
                        card
                    )
                )

                posted_at = (
                    self._extract_posted_at(
                        card.inner_text()
                    )
                )

                if not self._is_fresh(
                    posted_at
                ):

                    continue

                jobs.append(
                    {
                        "source": "NAUKRI",
                        "external_job_id": job_url,
                        "job_title": job_title,
                        "company_name": company_name,
                        "location": job_location,
                        "experience_min": experience_min,
                        "experience_max": experience_max,
                        "description": job_description,
                        "key_skills": key_skills,
                        "job_url": job_url,
                        "posted_at": posted_at,
                    }
                )

            except Exception as error:

                print(
                    f"Could not read search "
                    f"job {index + 1}: "
                    f"{error}"
                )

        return jobs

    # ---------------------------------------------------------
    # RECOMMENDED JOBS
    # ---------------------------------------------------------

    def _extract_recommended_jobs(
        self,
        page,
    ) -> list[dict]:

        jobs = []

        cards = page.locator(
            "div.cust-job-tuple.layout-wrapper.lay-1"
        )

        card_count = cards.count()

        print(
            f"Recommended job cards detected : "
            f"{card_count}"
        )

        if card_count == 0:

            print(
                "No recommended job cards "
                "were available."
            )

            return jobs

        homepage_url = (
            "https://www.naukri.com/"
            "mnjuser/homepage"
        )

        for index in range(
            card_count
        ):

            try:

                card = cards.nth(
                    index
                )

                title = card.locator(
                    "a.title"
                )

                company = card.locator(
                    ".comp-name"
                )

                location = card.locator(
                    ".loc"
                )

                job_title = (
                    title.inner_text().strip()
                    if title.count()
                    else ""
                )

                company_name = (
                    company.inner_text().strip()
                    if company.count()
                    else ""
                )

                job_location = (
                    location.inner_text().strip()
                    if location.count()
                    else ""
                )

                card_text = (
                    card.inner_text()
                )

                posted_at = (
                    self._extract_posted_at(
                        card_text
                    )
                )

                if not job_title:

                    continue

                print(
                    f"\nRecommended job "
                    f"{index + 1}:"
                )

                print(
                    f"  Title   : "
                    f"{job_title}"
                )

                print(
                    f"  Company : "
                    f"{company_name}"
                )

                print(
                    f"  Location: "
                    f"{job_location}"
                )

                if posted_at is None:

                    print(
                        "  Posted  : "
                        "posting age not detected"
                    )

                    print(
                        "  Status  : "
                        "SKIPPED - freshness unknown"
                    )

                    continue

                age = (
                    datetime.now()
                    - posted_at
                )

                print(
                    f"  Posted  : "
                    f"{posted_at}"
                )

                print(
                    f"  Age     : "
                    f"{age}"
                )

                if not self._is_fresh(
                    posted_at
                ):

                    print(
                        "  Status  : "
                        "SKIPPED - older than "
                        f"{MAX_FRESHNESS_DAYS} days"
                    )

                    continue

                # -------------------------------------------------
                # Reload homepage before opening
                # recommendation.
                # -------------------------------------------------

                if page.url != homepage_url:

                    page.goto(
                        homepage_url,
                        wait_until=(
                            "domcontentloaded"
                        ),
                        timeout=60000,
                    )

                    page.wait_for_timeout(
                        1500
                    )

                fresh_cards = page.locator(
                    "div.cust-job-tuple.layout-wrapper.lay-1"
                )

                if (
                    index
                    >= fresh_cards.count()
                ):

                    print(
                        "  Status  : "
                        "SKIPPED - card unavailable"
                    )

                    continue

                fresh_card = (
                    fresh_cards.nth(
                        index
                    )
                )

                fresh_title = (
                    fresh_card.locator(
                        "a.title"
                    )
                )

                if (
                    fresh_title.count()
                    == 0
                ):

                    print(
                        "  Status  : "
                        "SKIPPED - title link unavailable"
                    )

                    continue

                # -------------------------------------------------
                # Open job only.
                # Never click Apply.
                # -------------------------------------------------

                fresh_title.click()

                page.wait_for_timeout(
                    2500
                )

                detail_url = page.url

                if (
                    not detail_url
                    or detail_url
                    == homepage_url
                    or "job-listings"
                    not in detail_url
                ):

                    print(
                        "  Status  : "
                        "SKIPPED - real job URL "
                        "not obtained"
                    )

                    continue

                (
                    experience_min,
                    experience_max,
                ) = self._extract_experience(
                    detail_url
                )

                jobs.append(
                    {
                        "source":
                            "NAUKRI_RECOMMENDED",

                        "external_job_id":
                            detail_url,

                        "job_title":
                            job_title,

                        "company_name":
                            company_name,

                        "location":
                            job_location,

                        "experience_min":
                            experience_min,

                        "experience_max":
                            experience_max,

                        "description":
                            "",

                        "key_skills":
                            "",

                        "job_url":
                            detail_url,

                        "posted_at":
                            posted_at,
                    }
                )

                print(
                    f"  Detail URL : "
                    f"{detail_url}"
                )

                print(
                    "  Status     : "
                    "ACCEPTED"
                )

            except Exception as error:

                print(
                    f"Could not process "
                    f"recommended job "
                    f"{index + 1}: "
                    f"{error}"
                )

            finally:

                try:

                    page.goto(
                        homepage_url,
                        wait_until=(
                            "domcontentloaded"
                        ),
                        timeout=60000,
                    )

                    page.wait_for_timeout(
                        1000
                    )

                except Exception:

                    pass

        return jobs

    # ---------------------------------------------------------
    # MAIN DISCOVERY
    # ---------------------------------------------------------

    def fetch_jobs(
        self,
    ) -> list[dict]:

        role = (
            candidate_profile
            .target_roles[0]
        )

        location = (
            candidate_profile
            .preferred_locations[0]
        )

        print("=" * 60)

        print(
            "NAUKRI MULTI-SOURCE "
            "JOB DISCOVERY"
        )

        print("=" * 60)

        print(
            f"Role     : {role}"
        )

        print(
            f"Location : {location}"
        )

        print(
            f"Freshness : "
            f"{MAX_FRESHNESS_DAYS} days"
        )

        with sync_playwright() as playwright:

            context = (
                playwright.chromium
                .launch_persistent_context(
                    user_data_dir=str(
                        SESSION_DIR
                    ),
                    headless=False,
                )
            )

            page = (
                context.pages[0]
                if context.pages
                else context.new_page()
            )

            try:

                # -------------------------------------------------
                # OPEN NAUKRI
                # -------------------------------------------------

                print(
                    "\nOpening Naukri..."
                )

                page.goto(
                    self.BASE_URL,
                    wait_until=(
                        "domcontentloaded"
                    ),
                    timeout=60000,
                )

                page.wait_for_timeout(
                    3000
                )

                state = (
                    self._get_page_state(
                        page
                    )
                )

                print(
                    f"Page state : {state}"
                )

                # -------------------------------------------------
                # SECURITY
                # -------------------------------------------------

                if state in {
                    "CAPTCHA",
                    "OTP",
                }:

                    print(
                        "\nSecurity "
                        "verification detected."
                    )

                    print(
                        "Complete it manually "
                        "in the browser."
                    )

                    input(
                        "Press ENTER after "
                        "verification is complete..."
                    )

                    state = (
                        self._get_page_state(
                            page
                        )
                    )

                if state == (
                    "LOGIN_REQUIRED"
                ):

                    print(
                        "\nNaukri login "
                        "required."
                    )

                    print(
                        "Log in manually "
                        "in the browser."
                    )

                    print(
                        "Credentials are "
                        "not stored by this bot."
                    )

                    input(
                        "Press ENTER after "
                        "login is complete..."
                    )

                    state = (
                        self._get_page_state(
                            page
                        )
                    )

                if state in {
                    "CAPTCHA",
                    "OTP",
                }:

                    print(
                        "Security verification "
                        "still active."
                    )

                    return []

                # -------------------------------------------------
                # SOURCE 1 — SEARCH
                # -------------------------------------------------

                search_url = (
                    self._build_search_url(
                        role,
                        location,
                    )
                )

                print(
                    "\n"
                    + "=" * 60
                )

                print(
                    "SOURCE 1 : "
                    "NAUKRI SEARCH"
                )

                print(
                    f"Search URL : "
                    f"{search_url}"
                )

                page.goto(
                    search_url,
                    wait_until=(
                        "domcontentloaded"
                    ),
                    timeout=60000,
                )

                page.wait_for_timeout(
                    5000
                )

                state = (
                    self._get_page_state(
                        page
                    )
                )

                if state in {
                    "CAPTCHA",
                    "OTP",
                }:

                    print(
                        "Security verification "
                        "detected during Search."
                    )

                    return []

                search_jobs = (
                    self._extract_search_jobs(
                        page
                    )
                )

                print(
                    f"Fresh search jobs : "
                    f"{len(search_jobs)}"
                )

                # -------------------------------------------------
                # SOURCE 2 — RECOMMENDED
                # -------------------------------------------------

                print(
                    "\n"
                    + "=" * 60
                )

                print(
                    "SOURCE 2 : "
                    "NAUKRI RECOMMENDED"
                )

                page.goto(
                    "https://www.naukri.com/"
                    "mnjuser/homepage",
                    wait_until=(
                        "domcontentloaded"
                    ),
                    timeout=60000,
                )

                page.wait_for_timeout(
                    5000
                )

                state = (
                    self._get_page_state(
                        page
                    )
                )

                if state in {
                    "CAPTCHA",
                    "OTP",
                }:

                    print(
                        "Security verification "
                        "detected on Recommended."
                    )

                    print(
                        "Stopping safely."
                    )

                    return search_jobs

                recommended_jobs = (
                    self._extract_recommended_jobs(
                        page
                    )
                )

                print(
                    f"Fresh recommended jobs : "
                    f"{len(recommended_jobs)}"
                )

                # -------------------------------------------------
                # COMBINE
                # -------------------------------------------------

                all_jobs = (
                    search_jobs
                    + recommended_jobs
                )

                print(
                    "\n"
                    + "=" * 60
                )

                print(
                    "NAUKRI DISCOVERY SUMMARY"
                )

                print(
                    f"Search jobs       : "
                    f"{len(search_jobs)}"
                )

                print(
                    f"Recommended jobs  : "
                    f"{len(recommended_jobs)}"
                )

                print(
                    f"Total fresh jobs  : "
                    f"{len(all_jobs)}"
                )

                print("=" * 60)

                return all_jobs

            finally:

                context.close()


if __name__ == "__main__":

    source = NaukriSource()

    source.fetch_jobs()