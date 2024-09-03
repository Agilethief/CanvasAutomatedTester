from playwright.async_api import async_playwright
import asyncio
import os
from Playwright_Checks import check_course_is_valid


def start_session(courseID):
    asyncio.run(start_session_async(courseID))


async def start_session_async(courseID):
    print("browser session starting")
    async with async_playwright() as p:
        # initial setup
        browser = await p["chromium"].launch(headless=False)
        page = await browser.new_page()

        await log_into_canvas(page)
        await page.wait_for_timeout(1000)

        # Do everything else.

        # attempt to load the page
        # confirm the course is a valid course
        valid_course = await check_course_is_valid(page, courseID)
        if not valid_course:
            print("Invalid course")
            await browser.close()
            return

        print("Valid course, beginning checks")

        # Do some initial collection of data
        # Get all course Modules
        # Get all course pages
        # Get all course Assessments

        # Iterate through course pages

        # Iterate through assessments

        await browser.close()


async def log_into_canvas(page):
    await page.goto(f"{os.getenv('BASE_URL')}/login/canvas")

    await page.wait_for_selector("#pseudonym_session_unique_id")

    await page.fill("#pseudonym_session_unique_id", os.getenv("USER"))
    await page.get_by_label("Password").fill(os.getenv("PASS"))
    await page.get_by_role("button", name="Log in").click()

    await page.wait_for_timeout(1000)
    print("Logged in?")


def attempt_to_access_course():
    pass
