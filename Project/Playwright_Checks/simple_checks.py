import QA_Data
from playwright.async_api import async_playwright, Page
import os, requests, re


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
    extracted_id = re.search(pattern, url).group(1)
    return extracted_id


def extract_assessment_id_from_URL(url: str):
    pattern = r"assignments/(\d*)"
    extracted_id = re.search(pattern, url).group(1)
    return extracted_id
