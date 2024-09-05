import QA_Data
from playwright.async_api import async_playwright, Page
import re
from .simple_checks import confirm_on_page


# Top level, goes through all sub functions to populate the course object
async def start_page_checks(page: Page, page_object: QA_Data.Page):

    page_object.title = await get_page_title(page, page_object)
    page_object.word_count = await get_page_word_count(page, page_object)
    page_object.image_count = await check_page_images(page, page_object)

    page_links = await get_page_links(page, page_object)
    check_page_links(page_links, page_object)
    exit()


async def get_page_title(page: Page, page_object: QA_Data.Page):
    await confirm_on_page(page, page_object.url)

    is_title_visible = await page.locator(".page-title").is_visible()
    if not is_title_visible:
        print("Page does not have a title!")
        return

    return await page.locator(".page-title").inner_text()


async def get_page_word_count(page: Page, page_object: QA_Data.Page):
    await confirm_on_page(page, page_object.url)

    is_content_visible = await page.locator(".user_content").first.is_visible()
    if not is_content_visible:
        print("Page does not have user content!")
        return

    text_content = await page.locator(".user_content").first.all_inner_texts()
    text_content = text_content[0].replace("\n", " ")
    text_content = text_content.replace("\xa0", " ")
    word_count = len(text_content.split())
    # print("Word count:", word_count)
    return word_count


async def check_page_images(page: Page, page_object: QA_Data.Page):
    await confirm_on_page(page, page_object.url)

    is_content_visible = await page.locator(".user_content").first.is_visible()
    if not is_content_visible:
        print("Page does not have user content!")
        return

    img_list = []

    content_group = page.locator(".user_content").first

    image_elements = await content_group.locator("img").element_handles()

    for image in image_elements:
        src = await image.get_attribute("src")

        # Check if the src has the wrong course ID. flag this as an error!
        extracted_id = extract_id_from_URL(src)
        if int(extracted_id) != int(page_object.course.id):
            print(
                "image with incorrect course ID!",
                "found ID:",
                extracted_id,
                "   vs course ID:",
                page_object.course.id,
            )
            page_object.course.create_issue(
                "Image", "Image from a different course", src, page.url
            )

        img_list.append(image)

    return len(img_list)


async def get_page_links(page: Page, page_object: QA_Data.Page):
    await confirm_on_page(page, page_object.url)

    is_content_visible = await page.locator(".user_content").first.is_visible()
    if not is_content_visible:
        print("Page does not have user content!")
        return

    page_links = []

    content_group = page.locator(".user_content").first
    links = await content_group.locator("a").element_handles()

    for link in links:
        href = await link.get_attribute("href")
        title = await link.inner_text()
        internal = "https://wisdomlearning.instructure.com" in href

        page_links.append({"href": href, "title": title, "internal": internal})

    return page_links


def check_page_links(links, page_object: QA_Data.Page):
    for link in links:
        # print(link["title"], "  ", " Interal: ", link["internal"], "  ", link["href"])
        pass


def extract_id_from_URL(url: str):
    pattern = r"courses/(\d*)"
    extracted_id = re.search(pattern, url).group(1)
    return extracted_id
