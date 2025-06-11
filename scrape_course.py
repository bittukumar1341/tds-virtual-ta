import asyncio
from playwright.async_api import async_playwright
import json

URL = "https://tds.s-anand.net/#/2025-01/"

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)
        await page.wait_for_timeout(5000)

        sections = await page.evaluate("""
            () => Array.from(document.querySelectorAll('.reveal .slides section'))
                .map(sec => ({
                    heading: sec.querySelector('h2,h3,h4')?.innerText || '',
                    text: sec.innerText.trim()
                }))
        """)

        with open("course_content.json", "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)

        await browser.close()

asyncio.run(scrape())
