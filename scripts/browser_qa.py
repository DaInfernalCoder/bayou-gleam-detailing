#!/usr/bin/env python3
"""Small responsive smoke test for the Bayou Gleam static site."""

from playwright.sync_api import sync_playwright


URL = "http://127.0.0.1:4173"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        for width, height in ((1440, 1000), (1024, 900), (390, 844)):
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(URL, wait_until="load")
            page.locator("#workmanship").scroll_into_view_if_needed()
            page.wait_for_timeout(300)

            metrics = page.evaluate(
                """() => ({
                    viewport: innerWidth,
                    scrollWidth: document.documentElement.scrollWidth,
                    headerBackground:
                        getComputedStyle(document.querySelector(".site-header")).backgroundColor,
                    headerColor:
                        getComputedStyle(document.querySelector(".site-header")).color,
                    phoneLinks:
                        document.querySelectorAll('a[href="tel:+13466456236"]').length,
                    bookingLinks:
                        document.querySelectorAll(
                            'a[href="https://cal.com/sumitdatta/auto-detail-service"]'
                        ).length,
                    workmanshipImageWidth:
                        document.querySelector(".workmanship-photo img").naturalWidth
                })"""
            )
            print(f"{width}px: {metrics}")

            if width == 390:
                page.locator("[data-menu-toggle]").click()
                menu_state = page.locator("[data-nav]").evaluate(
                    """element => ({
                        open: element.classList.contains("is-open"),
                        display: getComputedStyle(element).display
                    })"""
                )
                expanded = page.locator("[data-menu-toggle]").get_attribute("aria-expanded")
                print(f"mobile menu: {menu_state}; aria-expanded={expanded}")
                page.locator("[data-menu-toggle]").click()

                page.locator("#faq details:first-child summary").click(force=True)
                faq_open = page.locator("#faq details:first-child").get_attribute("open")
                print(f"faq opens: {faq_open is not None}")

            page.close()

        browser.close()


if __name__ == "__main__":
    main()
