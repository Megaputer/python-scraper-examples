"""
### Downloads JavaScript generated content from web apps by using web browser
"""
import sys

from playwright.sync_api import sync_playwright, Error

from utils import InternetNode


def main():
    with InternetNode(__doc__) as node:
        if not node.url:
            raise SystemExit('Please provide at least one URL')

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.goto(node.url, wait_until='networkidle')
            except Error as exc:
                if 'net::ERR_ABORTED' in str(exc):
                    # see https://github.com/puppeteer/puppeteer/issues/2794
                    sys.stderr.write(f'Unable to download a file: {exc}')
                    sys.exit(2)
            else:
                node.insert(
                    page.url,
                    page.title(),
                    page.content(),
                )
                node.flush()
            finally:
                browser.close()


if __name__ == '__main__':
    main()
