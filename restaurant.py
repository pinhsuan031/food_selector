# pip install playwright 
# playwright install

import asyncio
from playwright.async_api import async_playwright

START_COORDS = (25.0338375,121.5429893)
RADIUS_KM = 1.0
SEARCH_QUERY = "中式"

async def main():
    async with async_playwright() as p:

        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"]) # 設為 True 則不顯示視窗
        context = await browser.new_context(no_viewport=True) # 讓視窗跟系統大小一致
        page = await context.new_page()

        # 直接導向中心點並搜尋
        url = f"https://www.google.com/maps/search/{SEARCH_QUERY}/@{START_COORDS[0]},{START_COORDS[1]},15z"
        await page.goto(url)
        await page.wait_for_selector('div[role="feed"]')

        input("按 Enter 關閉瀏覽器...")

asyncio.run(main())