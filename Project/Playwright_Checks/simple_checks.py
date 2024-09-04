import QA_Data
from playwright.async_api import async_playwright, Page
import os


def simple_check_connected():
    print("simple check connected")
    return True


async def confirm_on_page(page: Page, url: str):
    if page.url != url:
        # print("Wrong page:", page.url, "Is expected to be:", url)
        await page.goto(url)
        await page.wait_for_timeout(1000)
