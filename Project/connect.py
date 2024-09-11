from playwright.async_api import async_playwright
import asyncio
import os
from Playwright_Checks import (
    check_course_is_valid,
    get_course_data,
    start_assessment_checks,
    start_page_checks,
    clear_first_time_popups,
)
import QA_Data
import time
import generate_report


def start_session(course: QA_Data.Course):
    asyncio.run(start_session_async(course))


async def start_session_async(course: QA_Data.Course):
    start_time = time.time()

    # print("browser session starting")
    async with async_playwright() as p:
        # initial setup
        browser = await p["chromium"].launch(headless=True)

        # set cookies
        # browser_context = await browser.new_context()

        page = await browser.new_page()

        await log_into_canvas(page)
        await page.wait_for_timeout(1000)

        # Do everything else.

        # attempt to load the page
        # confirm the course is a valid course
        valid_course = await check_course_is_valid(page, course.id)
        if not valid_course:
            print("Invalid course")
            await browser.close()
            return

        # clear the annoying popup that tries to be a tutorial every time.
        await clear_first_time_popups(page)

        # Do some initial collection of data
        # Course Data
        await get_course_data(page, course)

        # Iterate through course pages
        # print("Page Checking:")
        for p in course.pages:
            await start_page_checks(page, p)

        # Iterate through assessments
        print("Assessment Checking:")
        for a in course.assessments:
            await start_assessment_checks(page, a)

        await browser.close()

        # print_results(course)
        generate_report.generate_excel_report(
            course, str(round(time.time() - start_time, 2))
        )
        print("--- %s seconds ---" % (round(time.time() - start_time, 2)))


# small utility just to print the results out
def print_results(course: QA_Data.Course):
    print("-===== RESULTS =====-")
    print("Course URL", course.url)
    print("Course title", course.title)
    print("Participants:", course.participant_count)
    print("Pages:", course.page_count)
    print("Modules:", course.module_count)
    print("Assessments:", course.assessment_count)

    for p in course.pages:
        print("Page:", p.title)
        print("Word count:", p.word_count)
        print("Image count:", p.image_count)

    for issue in course.issues:
        print(
            f"{issue.issue_type}: ",
            issue.issue_description,
            issue.issue_element,
            issue.issue_link,
        )


async def log_into_canvas(page):
    await page.goto(f"{os.getenv('BASE_URL')}/login/canvas")

    await page.wait_for_selector("#pseudonym_session_unique_id")

    await page.fill("#pseudonym_session_unique_id", os.getenv("USER"))
    await page.get_by_label("Password").fill(os.getenv("PASS"))
    await page.get_by_role("button", name="Log in").click()

    await page.wait_for_timeout(1000)
    print("Logged in")


def attempt_to_access_course():
    pass
