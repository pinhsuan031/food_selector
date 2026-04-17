from flask import Flask, render_template, request
import csv, random

# __name__ 用來定位目前載入資料夾的位置
app = Flask(__name__)

def get_all_types():
    types = set() # 使用 set 確保裡面不會有重複的字串
    try:
        with open('捷運大安站.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                types.add(row['type'])
    except FileNotFoundError:
        pass
    return list(types) # 轉回列表並排序，讓畫面顯示更整齊

def get_restaurants(selected_types=None):
    restaurants = []
    with open('捷運大安站.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not selected_types or row['type'] in selected_types:
                restaurants.append(row)
    return restaurants


@app.route('/say_hello')  # Python 內建的裝飾詞，讓Flask監聽此URL 並return 返還結果
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    # 1. 動態取得所有類型
    all_types = get_all_types()
    selected_types = request.form.getlist('restaurant_type')
    
    # 預設餐廳清單為空
    restaurants = []

    # 當使用者是透過 POST (按下按鈕) 且 確實有勾選東西時，才抓取資料
    if request.method == 'POST' and selected_types:

        # 根據勾選篩選餐廳
        selected_restaurants = get_restaurants(selected_types)
        k = min(3, len(selected_restaurants))
        restaurants = random.sample(selected_restaurants, k)
    
    return render_template('index.html', 
                           restaurants=restaurants, 
                           all_types=all_types, 
                           selected_types=selected_types)



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True, # 檔案更新網頁也會跟著更新
        port=5000
    )