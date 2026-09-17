from playwright.sync_api import sync_playwright

from application.browser_manager import BrowserManager


def main():
    with sync_playwright() as playwright:

        browser_manager = BrowserManager(playwright)

        page = browser_manager.start()

        page.goto("https://example.com")

        print("=" * 50)
        print("BROWSER TEST")
        print("=" * 50)
        print(f"Page title : {page.title()}")
        print(f"Page URL   : {page.url}")
        print("=" * 50)

        browser_manager.close()


if __name__ == "__main__":
    main()