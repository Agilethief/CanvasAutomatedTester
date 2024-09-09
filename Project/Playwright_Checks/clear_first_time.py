from playwright.async_api import async_playwright, Page


async def clear_first_time_popups(page: Page):

    # We set the local storage and then reload
    await page.evaluate(
        "window.localStorage.setItem('canvas-tourpoints-shown-admin', 'True');"
    )
    await page.evaluate(
        "window.localStorage.setItem('canvas-tourpoints-shown-teacher', 'True');"
    )

    page.reload()
