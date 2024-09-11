import QA_Data
from playwright.async_api import async_playwright, Page
import re
from .simple_checks import (
    confirm_on_page,
    get_word_count,
    get_image_count_and_check,
    check_links,
    get_page_links,
)


# Top level, goes through all sub functions to populate the course object
async def start_page_checks(page: Page, page_object: QA_Data.Page):

    page_object.title = await get_page_title(page, page_object)
    page_object.word_count = await get_word_count(page)
    page_object.image_count = await get_image_count_and_check(
        page, page_object, page_object
    )
    page_object.published = await check_page_published(page, page_object)

    page_links = await get_page_links(page)
    page_object.link_count = len(page_links)
    check_links(page_links, page_object, page_object, page_object.course)


async def get_page_title(page: Page, page_object: QA_Data.Page):
    await confirm_on_page(page, page_object.url)

    is_title_visible = await page.locator(".page-title").first.is_visible()
    if not is_title_visible:
        print("Page does not have a title!")
        return

    return await page.locator(".page-title").first.inner_text()


async def check_page_published(page: Page, page_object: QA_Data.Page):
    await confirm_on_page(page, page_object.url)

    is_publish_visible = await page.locator(".btn-publish").is_visible()
    is_published_visible = await page.locator(".btn-published").is_visible()

    if is_publish_visible:
        # print("Page has a publish button! - Likely unpublished")
        return False

    if is_published_visible:
        # print("Page does not have a publish button! - Likely published")
        return True

    # print("No publish information found for the page")
    return False
