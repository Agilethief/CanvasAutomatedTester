import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect, Page
from dotenv import load_dotenv
import os


@pytest.fixture(scope="function", autouse=True)
def load_env():
    load_dotenv()
    print("Env loaded before test runs")


def test_canvas_login(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://wisdomlearning.instructure.com/login/canvas")
    page.screenshot(path=f"test_login.png", full_page=True)

    page.query_selector("#pseudonym_session_unique_id").fill(os.getenv("USER"))
    page.get_by_label("Password").fill(os.getenv("PASS"))
    page.get_by_role("button", name="Log in").click()

    page.wait_for_timeout(1000)

    expect(page.locator("#dashboard_header_container")).to_contain_text("Dashboard")
    # page.get_by_role("button", name="Admin").click()
    # expect(page.locator("#global_nav_accounts_link")).to_contain_text("Admin")

    # ---------------------
    context.close()
    browser.close()
