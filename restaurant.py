import asyncio, random, math, os
import pandas as pd
from playwright.async_api import async_playwright


# 計算地圖上兩點距離
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# 讀取已經寫入檔案的店家連結，避免寫入重複店家
def get_seen_links(file_name):
    file_path = f"{file_name}.csv"
    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        seen_links = set(old_df["link"])
    else:
        seen_links = set()
    return seen_links

# 將查詢結果寫入 csv 檔
def write_to_csv(file_name, info):
    file_path = f"{file_name}.csv"
    pd.DataFrame(info).to_csv(file_path, mode="a", index=False, encoding="utf-8-sig", header=not os.path.exists(file_path), lineterminator="\n")

# 爬取資料
async def scrape_restaurant(file_name, center, search_query, radius_m):
    async with async_playwright() as p:

        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"]) # headless 設為 True 則不顯示視窗
        context = await browser.new_context(no_viewport=True) # 讓視窗跟系統大小一致
        page = await context.new_page()

        # 將連結導向中心點
        url = f"https://www.google.com/maps/@{center[0]},{center[1]},16.5z"
        await page.goto(url)
        await asyncio.sleep(3)

        seen_links = get_seen_links(file_name) # 已經查詢過的店家連結
        results = [] # 存取結果的list

        # 搜尋關鍵字
        for query in search_query:
            search_box = page.locator('input[role="combobox"]')
            await search_box.wait_for()
            await search_box.click()
            await search_box.fill(query)
            await asyncio.sleep(1.5)
            await search_box.press("Enter")
            await page.wait_for_selector('div[role="feed"]')
            await asyncio.sleep(3)

            # 模擬捲動以加載更多內容
            print(f"搜尋關鍵字為 {query}")
            # 定位側欄容器
            scroller = page.locator('div[role="feed"]')
            for _ in range(5):
                await scroller.evaluate("node => node.scrollBy(0, 2000)")
                await asyncio.sleep(random.uniform(3.0, 5.0)) # 隨機延遲預防封鎖
                lists = await page.locator('div[role="article"]').count()

            # 抓取所有餐廳卡片
            lists = await page.query_selector_all('div[role="article"]')
            
            # 抓取每間餐廳的資料
            for entry in lists:
                # 1. 抓取店名與連結
                name_element = await entry.query_selector('a')
                name = await name_element.get_attribute('aria-label')
                link = await name_element.get_attribute('href')
                # 判斷抓取店家是否重複，如果重複則跳過
                if link in seen_links:
                    continue
                seen_links.add(link)

                # 2. 從連結中解析座標並計算距離
                # Google Maps 連結包含 !3d緯度!4d經度
                lat = float(link.split("!3d")[1].split("!4d")[0])
                lng = float(link.split("!4d")[1].split("!")[0])
                distance = haversine(center[0], center[1], lat, lng)
                # 如果距離大於設定範圍則跳過
                if distance > radius_m:
                    continue

                # 3. 抓取評分
                # Google 的 CSS Class 可能隨時變動，此處使用相對位置獲取
                # 有些店家可能沒有評分
                try: 
                    rating_detail = await entry.query_selector_all('span.fontBodyMedium > span > span')
                    rating = await rating_detail[0].inner_text()
                except Exception as e:
                    rating = "無資料"
                    print(e)

                # 4. 抓取價位
                # 有些店家可能沒有標示價位
                try: 
                    price_detail = await entry.query_selector_all('div.AJB7ye > span > span')
                    price = await price_detail[2].inner_text()
                except Exception as e:
                    price = "無資料"
                    print(e)

                # 5. 寫入 result
                results.append({
                    "name": name, 
                    "type": query,
                    "rating": rating, 
                    "price": price,
                    "link": link, 
                    "distance": round(distance), 
                    "lat": lat,
                    "lng": lng
                })

        
        return results


# 匯入變數
with open("input.txt", mode="r", encoding="utf-8") as f:
    var = f.readlines()

# 想要存入的檔案名稱，建議使用起始點名稱
file_name = var[0].strip()
# 起始點座標
center = var[1].strip().split(',')
for i in range(2):
    center[i] = eval(center[i])
# 搜尋字詞
search_query = var[2].strip().split(',')
search_query = list(search_query)
# 篩選自訂範圍內的店家，單位為公尺
radius_m = eval(var[3])


# 主程式
try: 
    restaurant_info = asyncio.run(scrape_restaurant(file_name, center, search_query, radius_m))
except Exception as e:
    print(e)

write_to_csv(file_name, restaurant_info)
