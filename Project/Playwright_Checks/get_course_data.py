import QA_Data
from playwright.async_api import async_playwright, Page
import os, re
from .simple_checks import confirm_on_page, extract_assessment_id_from_URL

# this script handles getting the top level course data
# - ID : int
# - Title : string
# - Participant count : int
# - Page count : int
# - Assessment count : int
# - link count : int
# - Image count : int
# - Modules[] : Module
# - Pages []: Page
# - Assessments[] : Assessment

"""
This will transform the course object that is passed into it.
"""


# Top level, goes through all sub functions to populate the course object
async def get_course_data(page: Page, course_object: QA_Data.Course):
    # Course
    course_object.set_url(f"{os.getenv('BASE_URL')}/courses/{course_object.id}")
    await get_course_title(page, course_object)
    await get_course_participant_count(page, course_object)

    # Page setup
    await get_course_page_count(page, course_object)
    page_links = await get_course_page_urls(page, course_object)
    create_pages_from_links(page_links, course_object)

    # Module setup
    await get_course_module_count(page, course_object)

    # Assessment setup
    await get_course_assessment_count(page, course_object)
    assessment_data = await get_course_assessment_urls(page, course_object)
    create_assessments_from_data(assessment_data, course_object)


async def get_course_title(page: Page, course_object: QA_Data.Course):
    # Make sure we are on the right page.
    await confirm_on_page(page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}")

    foundTitle = await page.locator(".course-title").is_visible()
    if foundTitle:
        courseTitle = await page.locator(".course-title").inner_text()
        title_text = courseTitle
    else:
        title_text = "No title found"

    course_object.set_title(title_text)
    return title_text


async def get_course_participant_count(page: Page, course_object: QA_Data.Course):
    # Navigate to the users page
    await confirm_on_page(
        page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}/users"
    )

    role_texts = page.locator('[name="enrollment_role_id"]')

    # TODO: Make this generic and a utility
    # Retrieve inner text of the student locator
    selection_text = await role_texts.inner_text()
    selection_text = selection_text.split("\n")
    student_text = "Not found"
    for item in selection_text:
        if "Student" in item:
            student_text = item
            break

    pattern = r"\d+\d*"
    participant_count = re.findall(pattern, student_text)

    course_object.set_participant_count(participant_count[0])
    return participant_count


async def get_course_page_count(page: Page, course_object: QA_Data.Course):
    await confirm_on_page(
        page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}/pages"
    )

    page_count = await page.locator(".wiki-page-title").count()

    course_object.set_page_count(page_count)
    return page_count


async def get_course_page_urls(page: Page, course_object: QA_Data.Course):
    await confirm_on_page(
        page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}/pages"
    )
    page_links = []

    page_group = page.locator(".collectionViewItems")
    page_items = page_group.locator(".wiki-page-title")
    links = await page_items.locator("a").element_handles()

    for link in links:
        href = await link.get_attribute("href")
        page_links.append(href)
        # print(href)

    return page_links


def create_pages_from_links(links: list[str], course_object: QA_Data.Course):
    for link in links:
        newPage = QA_Data.Page(link, course_object)

        course_object.pages.append(newPage)


async def get_course_module_count(page: Page, course_object: QA_Data.Course):
    await confirm_on_page(
        page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}/modules"
    )

    module_count = await page.locator(".context_module").count()

    course_object.set_module_count(module_count)
    return module_count


# Arguably redundant with the implementation of URL grabbing below.
async def get_course_assessment_count(page: Page, course_object: QA_Data.Course):
    await confirm_on_page(
        page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}/assignments"
    )

    assessment_count = await page.locator(".assignment").count()

    course_object.set_assessment_count(assessment_count)
    return assessment_count


async def get_course_assessment_urls(page: Page, course_object: QA_Data.Course):
    await confirm_on_page(
        page, f"{os.getenv('BASE_URL')}/courses/{course_object.id}/assignments"
    )
    assessment_data = []

    assessment_group = page.locator("#ag-list")
    assessment_items = assessment_group.locator(".ig-info")
    links = await assessment_items.locator("a").element_handles()

    for link in links:
        href = await link.get_attribute("href")
        title = await link.inner_text()
        # Detect if it is an edit link, and if so remove the edit section so we have a pure link
        aa_id = extract_assessment_id_from_URL(href)
        reconstructed_link = (
            f"{os.getenv('BASE_URL')}/courses/{course_object.id}/assignments/{aa_id}"
        )

        assessment_data.append(
            {"link": reconstructed_link, "title": title, "id": aa_id}
        )
        # print(href)

    return assessment_data


def create_assessments_from_data(aa_data, course_object: QA_Data.Course):
    for aa in aa_data:
        newAssessment = QA_Data.Assessment(aa["id"], aa["title"], course_object)
        newAssessment.url = aa["link"]

        course_object.assessments.append(newAssessment)
