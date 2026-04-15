# pip install playwright 
# playwright install

import asyncio
import random
import math
import re
from playwright.async_api import async_playwright

center = (25.0336646, 121.5438858) # 起始點為捷運大安站
radius_m = 800 # 篩選半徑800公尺內店家
search_query = "日式"

# 生成2x2網格
def generate_2x2_grid(center):
    lat, lng = center
    offset_lat = 0.0036  # 約 400 公尺
    offset_lng = 0.0040  # 約 400 公尺
    
    return [
        [lat + offset_lat, lng + offset_lng], # 東北
        [lat + offset_lat, lng - offset_lng], # 西北
        [lat - offset_lat, lng + offset_lng], # 東南
        [lat - offset_lat, lng - offset_lng]  # 西南
    ]

# 計算距離
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))


async def scrape_restaurant():
    async with async_playwright() as p:

        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"]) # 設為 True 則不顯示視窗
        context = await browser.new_context(no_viewport=True) # 讓視窗跟系統大小一致
        page = await context.new_page()

        # 將連結導向中心點並搜尋
        grid_point = generate_2x2_grid(center)[0]
        url = f"https://www.google.com/maps/@{grid_point[0]},{grid_point[1]},17z"
        await page.goto(url)
        await asyncio.sleep(3)

        search_box = page.locator('input[role="combobox"]')
        await search_box.wait_for()
        await search_box.fill(search_query)
        await asyncio.sleep(1)
        await search_box.press("Enter")
        await page.wait_for_selector('div[role="feed"]')

        # 模擬捲動以加載更多內容
        print("正在加載地圖資料...")
        # 定位側欄容器
        scroller = page.locator('div[role="feed"]')
        for _ in range(3):
            await asyncio.sleep(random.uniform(3.0, 5.0)) # 隨機延遲預防封鎖
            await scroller.evaluate("node => node.scrollBy(0, 2000)")
            cards = await page.locator('div[role="article"]').count()
            print(f"目前偵測到 {cards} 家餐廳")

        lists = await page.query_selector_all('div[role="article"]')

        for entry in lists[:5]:
            # 1. 店名與連結
            name_element = await entry.query_selector('a')
            name = await name_element.get_attribute('aria-label')
            link = await name_element.get_attribute('href')
            print(name, link)

            # 2. 從連結中解析座標 (正規表示法)
            # Google Maps 連結通常包含 !3d緯度!4d經度
            lat = float(link.split("!3d")[1].split("!4d")[0])
            lng = float(link.split("!4d")[1].split("!")[0])
            distance = haversine(center[0], center[1], lat, lng)
            print(distance)
            # if distance > 800:
            #     continue

            # 3. 評分
            # 注意：Google 的 CSS Class 可能隨時變動，此處使用相對位置獲取
            
            rating_detail = await entry.query_selector_all('span.fontBodyMedium > span > span')
            rating = await rating_detail[0].inner_text()
            print(rating)


            # 4. 價位
            price_detail = await entry.query_selector_all('div.AJB7ye > span > span')
            price = await price_detail[2].inner_text()
            print(price)



        input("按 Enter 關閉瀏覽器...")

asyncio.run(scrape_restaurant())