from playwright.async_api import async_playwright
import os


# tests - ID 1 is a fail, ID 700 is a success
async def check_course_is_valid(page, courseID):
    await page.goto(f"{os.getenv('BASE_URL')}/courses/{courseID}")

    await page.wait_for_timeout(1000)

    # Check if the error page is visible
    is_error_page = await page.locator(".ic-Error-page").is_visible()

    # Return the opposite of is_error_page since it should return False if the error page is found
    return not is_error_page
