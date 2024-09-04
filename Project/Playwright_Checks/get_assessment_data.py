import QA_Data
from playwright.async_api import async_playwright, Page
import os
from .simple_checks import confirm_on_page


# Top level, goes through all sub functions to populate the course object
async def get_assessment_data(page: Page, assessment_object: QA_Data.Assessment):

    # assessment_object
    await get_build_settings(page, assessment_object)
    pass


async def get_build_settings(page: Page, assessment_object: QA_Data.Assessment):
    await confirm_on_page(page, assessment_object.url)
