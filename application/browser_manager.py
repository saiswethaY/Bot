from pathlib import Path

from playwright.sync_api import (
    BrowserContext,
    Page,
    Playwright,
)


class BrowserManager:
    def __init__(self, playwright: Playwright):
        self.playwright = playwright
        self.context: BrowserContext | None = None
        self.page: Page | None = None

        self.session_dir = (
            Path(__file__).resolve().parent.parent
            / ".browser_session"
            / "naukri"
        )

    def start(self) -> Page:
        self.session_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        print("=" * 60)
        print("BROWSER SESSION")
        print("=" * 60)
        print(f"Session directory: {self.session_dir}")
        print("Using persistent Naukri browser session.")
        print("=" * 60)

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_dir),
            headless=False,
            viewport=None,
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        return self.page

    def close(self) -> None:
        if self.context is not None:
            self.context.close()

        self.page = None
        self.context = None