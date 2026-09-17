from playwright.sync_api import sync_playwright

from application.browser_manager import BrowserManager
from application.page_inspector import print_page_inspection


def main():
    with sync_playwright() as playwright:

        browser_manager = BrowserManager(playwright)

        page = browser_manager.start()

        page.goto("https://example.com")

        print_page_inspection(page)

        browser_manager.close()


if __name__ == "__main__":
    main()