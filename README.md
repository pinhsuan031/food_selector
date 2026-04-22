# Food Selector
今天吃什麼？不用再煩惱了。

只要選擇想吃的類型，系統就會從附近餐廳中隨機挑出三個選項，快速幫你做決定。
也可以自訂地點，抓取 Google 地圖上的餐廳資料，探索不同地區的美食。

## 套件列表
- pandas
- playwright
- flask
- 標準函式庫
  - asyncio
  - random
  - math
  - os
  - csv

## 程式使用方法
### 啟動推薦網頁
1. 執行 `app.py`
2. 開啟瀏覽器並輸入 `localhost:5000` 進入首頁
3. 在介面上選擇餐廳類型，系統將隨機推薦三家餐廳
4. 互動功能：
  - 點擊「餐廳資訊卡」可在地圖查看位置
  - 點擊「餐廳名稱」可直接連結至 Google 地圖

### 抓取不同位置的餐廳資料
若欲更改推薦的地理區域，請依照下列步驟操作：
1. **設定搜尋參數：** 在 `input.txt` 中輸入想查詢的「位置名稱」、「經緯度」、「關鍵字」與「篩選範圍」
2. **執行抓取腳本：** 執行 `restaurant.py`，程式會自動至 Google 地圖查詢並篩選指定範圍內的餐廳，最後將資料存入 CSV 檔
3. **變更網頁資料來源：**
 - 在 `app.py` 中修改 file_name 變數，指向新的 CSV 檔案
 - 在 `static/map.js` 中修改 lat 與 lng 變數，變更地圖的中心點座標

### 檔案架構
- `static/`
  - `map.js`: 初始化 leaflet 地圖
  - `style.css`: `index.html` 引用的樣式表
- `templates/`
  - `index.html`: 主頁面的網頁 HTML
- `app.py`: 用於啟動 Flask 網頁伺服器
- `input.txt`: 存放抓取餐廳時所需的關鍵字、經緯度及篩選範圍
- `restaurant.py`: 抓取 Google 地圖餐廳資料的程式
