from playwright.sync_api import sync_playwright

from application.browser_manager import BrowserManager
from application.safety_gate import check_page_safety


def main():
    with sync_playwright() as playwright:

        browser_manager = BrowserManager(playwright)

        page = browser_manager.start()

        page.goto("https://example.com")

        result = check_page_safety(page)

        print("=" * 50)
        print("SAFETY GATE TEST")
        print("=" * 50)
        print(f"Page type : TEST_PAGE")
        print(f"Decision  : {result}")
        print("=" * 50)

        browser_manager.close()


if __name__ == "__main__":
    main()