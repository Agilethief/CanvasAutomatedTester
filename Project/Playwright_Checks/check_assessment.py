import QA_Data
from playwright.async_api import (
    async_playwright,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)
import os
from .simple_checks import (
    confirm_on_page,
    get_word_count,
    get_image_count_and_check,
    check_links,
    get_page_links,
)


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

    await confirm_on_page(page, f"{assessment_object.url}")

    await page.wait_for_timeout(4000)
    frame = page.frame_locator(".tool_launch")

    frame_body_visible = await frame.locator("body").is_visible()

    if not frame_body_visible:
        print("frame is not ready or found")
        return
    # Now we should be properly loaded into the assessment.
    # Get user content blocks
    # user_content = await frame.locator(".user_content").all()

    # Question count
    assessment_object.question_count = (
        await frame.locator(".closedItems").locator(">div").count()
    )

    # Link check
    links = await get_page_links(frame)
    assessment_object.link_count = len(links)

    check_links(links, assessment_object, assessment_object, assessment_object.course)

    # Word checks
    assessment_object.word_count = await get_word_count(frame)

    # Image checks
    assessment_object.image_count = await get_image_count_and_check(
        frame, assessment_object, assessment_object
    )

    # build on last attempt check
    assessment_object.build_on_last_attempt = await check_build_on_last_attempt(
        page, assessment_object
    )


async def check_build_on_last_attempt(
    page: Page, assessment_object: QA_Data.Assessment
):
    await confirm_on_page(page, f"{assessment_object.url}")

    frame = page.frame_locator(".tool_launch")

    # TODO: Handle this better
    await page.wait_for_timeout(4000)

    # get the header locator
    # find the locator inside with the text "settings"
    try:
        print("Entering settings")
        header_locator = frame.locator(".header")
        await header_locator.locator('div[role="tab"]:has-text("Settings")').wait_for(
            state="visible", timeout=5000
        )
        await header_locator.locator('div[role="tab"]:has-text("Settings")').click()
        await page.wait_for_timeout(1000)

        # Get the multiple attemps box.
        # Because of how it is built, we can't just check the input (it is always true!)
        # Instead we read the name of the SVG IconX or IconCheck
        label_locator = frame.locator('label:has-text("Allow multiple attempts")')
        await label_locator.wait_for()
        # print(await label_locator.first.get_attribute("for")) # Just used to confirm we are getting the right locator

        name_of_toggle = await label_locator.locator("svg").first.get_attribute("name")
        # print(name_of_toggle)
        if name_of_toggle == "IconCheck":
            # print("Successfully found the toggle and it is checked")
            build_on_last_attempt_label_locator = frame.locator(
                'label:has-text("Enable build on last attempt")'
            )
            build_on_last_attempt_visible = (
                await build_on_last_attempt_label_locator.locator("svg").is_visible()
            )
            # print("BOLA", build_on_last_attempt_visible)
            return build_on_last_attempt_visible

        return "No multiple attempt"

    except PlaywrightTimeoutError:
        print("No settings on this page.")
        return "Unable to get settings"
