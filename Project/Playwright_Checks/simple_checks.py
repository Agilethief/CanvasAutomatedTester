import QA_Data
from playwright.async_api import async_playwright, Page
import os, requests, re

import QA_Data.I_Statable


def simple_check_connected():
    print("simple check connected")
    return True


async def confirm_on_page(page: Page, url: str):
    if page.url != url:
        # print("Wrong page:", page.url, "Is expected to be:", url)
        await page.goto(url)
        await page.wait_for_timeout(1000)


def test_link_response(url):
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code <= 299:
        return True

    return False


def extract_id_from_URL(url: str):
    pattern = r"courses/(\d*)"

    match_found = re.search(pattern, url)

    if match_found:
        # extracted_id = re.search(pattern, url).group(1)
        extracted_id = match_found.group(1)
        return extracted_id
    else:
        # print("url had no course id")
        return 0


def extract_assessment_id_from_URL(url: str):
    pattern = r"assignments/(\d*)"
    extracted_id = re.search(pattern, url).group(1)
    return extracted_id


async def get_word_count(base_locator):

    user_content = await base_locator.locator(".user_content").all()

    text_content = ""
    for uc in user_content:
        for uc_text in await uc.all_inner_texts():
            text_content = text_content + " " + uc_text

    text_content = text_content.replace("\n", " ")
    text_content = text_content.replace("\xa0", " ")
    word_count = len(text_content.split())
    return word_count


async def get_image_count_and_check(
    base_locator,
    statable: QA_Data.I_Statable,
    issuable: QA_Data.I_Issuable,
):
    image_list = []
    user_content = await base_locator.locator(".user_content").all()
    for uc in user_content:
        image_elements = await uc.locator("img").element_handles()
        for image in image_elements:
            src = await image.get_attribute("src")
            if check_image(src, statable, issuable):
                image_list.append(image)

    return len(image_list)


def check_image(
    image_src,
    statable: QA_Data.I_Statable,
    issuable: QA_Data.I_Issuable,
):
    # print(image_src)
    # Make sure it is a real image and not some Canvas based graphic or icon
    if image_src is None:
        return False

    if len(image_src) < 10:
        return False

    # Check if the src has the wrong course ID. flag this as an error!
    extracted_id = extract_id_from_URL(image_src)
    if int(extracted_id) != int(statable.get_course().id):
        issuable.create_issue(
            "Image",
            "Image from a different course",
            image_src,
            statable.get_url(),
            statable.get_title(),
        )

    return True


async def get_page_links(base_locator):
    page_links = []
    link_el = []

    user_content = await base_locator.locator(".user_content").all()
    for uc in user_content:
        for link in await uc.locator("a").element_handles():
            link_el.append(link)

    for link in link_el:
        if link is None:
            continue

        # clean up download icons that double up the links
        link_classes = await link.get_attribute("class")
        if link_classes is not None:
            if "file_download_btn" in link_classes.split():
                # print("skipping download button")
                continue

        href = await link.get_attribute("href")
        # dirty guard
        if href is None:
            # print(link, "has no href?")
            continue

        title = await link.inner_text()
        internal = "https://wisdomlearning.instructure.com" in href

        page_links.append({"href": href, "title": title, "internal": internal})

    return page_links


def check_links(
    links,
    statable: QA_Data.I_Statable,
    issuable: QA_Data.I_Issuable,
    course: QA_Data.Course,
):
    for link in links:
        # print(link["title"], "  ", " Interal: ", link["internal"], "  ", link["href"])
        if link["internal"]:
            check_internal_link(link["href"], statable, issuable, course)
            return

        # Checking external links.
        if "https:" in link["href"]:
            check_external_link(link["href"], statable, issuable)
            return


def check_internal_link(
    link,
    statable: QA_Data.I_Statable,
    issuable: QA_Data.I_Issuable,
    course: QA_Data.Course,
):
    link_course_id = extract_id_from_URL(link)
    if int(link_course_id) != int(course.id):
        # print("bad internal link!", link)
        issuable.create_issue(
            "Bad internal link",
            f"Link from a different course {link_course_id}, should be linked to {course.id}",
            link,
            statable.get_url(),
            statable.get_title(),
        )
        return

    if not test_link_response(link):
        issuable.create_issue(
            "AA Bad internal link",
            "Link did not resolve",
            link,
            statable.get_url(),
            statable.get_title(),
        )
        return


def check_external_link(
    link,
    statable: QA_Data.I_Statable,
    issuable: QA_Data.I_Issuable,
):
    if "https:" not in link:
        return

    if not test_link_response(link):
        # print("bad externak link!")
        issuable.create_issue(
            "AA Bad external link",
            "Link did not resolve",
            link,
            statable.get_url(),
            statable.get_title(),
        )
        return
