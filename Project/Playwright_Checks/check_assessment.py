import QA_Data
from playwright.async_api import async_playwright, Page
import os
from .simple_checks import confirm_on_page, test_link_response, extract_id_from_URL


# Top level, goes through all sub functions to populate the course object
async def start_assessment_checks(page: Page, assessment_object: QA_Data.Assessment):

    print("AA:", assessment_object.title)
    # assessment_object
    await get_build_settings(page, assessment_object)
    await check_assessment_page(page, assessment_object)

    # exit()
    assessment_object.print_stats()


async def get_build_settings(page: Page, assessment_object: QA_Data.Assessment):
    await confirm_on_page(page, f"{assessment_object.url}/edit")

    # Points
    assessment_object.points = await page.locator(
        "#assignment_points_possible"
    ).input_value()

    # AA Group
    aa_selected_group_locator = page.locator("#assignment_group_id")
    aa_selected_group_id = await aa_selected_group_locator.input_value()
    aa_selected_group_option_locator = aa_selected_group_locator.locator(
        f'option[value="{aa_selected_group_id}"]'
    )
    assessment_object.group = await aa_selected_group_option_locator.inner_text()

    # Mark Display
    assessment_object.mark_display = await page.locator(
        "#assignment_grading_type"
    ).input_value()

    # If the grading scheme is visible, we process it
    grading_scheme_visible = await page.locator(
        "#grading-schemes-selector-dropdown"
    ).is_visible()
    if grading_scheme_visible:
        assessment_object.grading_scheme = await page.locator(
            "#grading-schemes-selector-dropdown"
        ).input_value()
    else:
        assessment_object.grading_scheme = "Not set"

    # Due Date
    due_date_container = (
        page.locator(".css-oyjt6a-dateInput").filter(has_text="Due Date").first
    )
    assessment_object.due_date = await due_date_container.locator("input").input_value()
    # Release Date
    release_date_container = (
        page.locator(".css-oyjt6a-dateInput").filter(has_text="Available from").first
    )
    assessment_object.release_date = await release_date_container.locator(
        "input"
    ).input_value()

    # Published
    publish_text = await page.locator("#assignment-draft-state").inner_text()
    if "Not" in publish_text:
        assessment_object.published = False
    else:
        assessment_object.published = True


async def check_assessment_page(page: Page, assessment_object: QA_Data.Assessment):
    frame = page.frame_locator(".tool_launch")
    # iframe_locator = await page.wait_for_selector("iframe")
    # await iframe_locator.content_frame()  # should help insist the iframe is correctly loaded

    await page.wait_for_timeout(4000)
    await frame.locator(".overlay").first.is_visible()

    # Now we should be properly loaded into the assessment.

    # Link check
    links = await get_assessment_links(page, assessment_object)
    check_assessment_links(links, assessment_object)

    # Word checks

    # Image checks

    # build on last attempt check
    assessment_object.build_on_last_attempt = await check_build_on_last_attempt(
        page, assessment_object
    )


async def get_assessment_links(page: Page, assessment_object: QA_Data.Assessment):
    await confirm_on_page(page, f"{assessment_object.url}")

    # Get the body of the assessment questions from the iframe.
    frame = page.frame_locator(".tool_launch")

    page_links = []
    link_el = await frame.locator("a").element_handles()
    # print(link_el, "link el len:", len(link_el))

    for link in link_el:
        href = await link.get_attribute("href")
        # dirty guard
        if href is None:
            print(link, "has no href?")
            continue

        title = await link.inner_text()
        internal = "https://wisdomlearning.instructure.com" in href

        page_links.append({"href": href, "title": title, "internal": internal})
        assessment_object.link_count += 1

    return page_links


def check_assessment_links(links, assessment_object: QA_Data.Assessment):
    for link in links:
        # print(link["title"], "  ", " Interal: ", link["internal"], "  ", link["href"])
        if link["internal"]:
            check_internal_link(
                link["href"], assessment_object, assessment_object.course
            )
            return

        # Checking external links.
        if "https:" in link["href"]:
            check_external_link(
                link["href"], assessment_object, assessment_object.course
            )
            return


def check_internal_link(link, assessment: QA_Data.Assessment, course: QA_Data.Course):
    link_course_id = extract_id_from_URL(link)
    if int(link_course_id) != int(course.id):
        # print("bad internal link!", link)
        assessment.create_issue(
            "Bad internal link",
            f"Link from a different course {link_course_id}, should be linked to {course.id}",
            link,
            assessment.url,
            assessment.title,
        )
        return

    if not test_link_response(link):
        assessment.create_issue(
            "AA Bad internal link",
            "Link did not resolve",
            link,
            assessment.url,
            assessment.title,
        )
        return


def check_external_link(link, assessment: QA_Data.Assessment, course: QA_Data.Course):
    if "https:" not in link:
        return

    if not test_link_response(link):
        # print("bad externak link!")
        assessment.create_issue(
            "AA Bad external link",
            "Link did not resolve",
            link,
            assessment.url,
            assessment.title,
        )
        return


async def check_build_on_last_attempt(
    page: Page, assessment_object: QA_Data.Assessment
):
    await confirm_on_page(page, f"{assessment_object.url}")

    frame = page.frame_locator(".tool_launch")

    # TODO: Handle this better
    await page.wait_for_timeout(4000)
    await frame.locator(".overlay").first.wait_for()

    # get the header locator
    # find the locator inside with the text "settings"
    try:
        print("Entering settings")
        header_locator = frame.locator(".header")
        await header_locator.locator('div[role="tab"]:has-text("Settings")').wait_for()
        await header_locator.locator('div[role="tab"]:has-text("Settings")').click()

        await frame.get_by_role("checkbox", name="Allow multiple attempts").wait_for()
        multiple_attempts = await frame.get_by_role(
            "checkbox", name="Allow multiple attempts"
        ).input_value()
        print("MA", multiple_attempts)

        if multiple_attempts:
            await frame.get_by_role(
                "checkbox", name="Enable build on last attempt"
            ).wait_for()
            build_on_last_attempt = await frame.get_by_role(
                "checkbox", name="Enable build on last attempt"
            ).input_value()
            print("BoLA", build_on_last_attempt)
            return build_on_last_attempt
    except TimeoutError:
        print("No settings on this page.")

    await page.wait_for_timeout(10000)
    exit()
    return "Not set"
