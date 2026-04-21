from flask import Flask, render_template, request, jsonify
import csv, random

# __name__ 用來定位目前載入資料夾的位置
app = Flask(__name__)

file_name = '捷運大安站.csv'

def get_all_types():
    types = set() # 使用 set 確保裡面不會有重複的字串
    try:
        with open(file_name, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                types.add(row['type'])
    except FileNotFoundError:
        pass
    return sorted(list(types)) # 轉回列表並排序，讓畫面顯示更整齊

def get_restaurants(selected_types=None):
    restaurants = []
    with open(file_name, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not selected_types or row['type'] in selected_types:
                restaurants.append(row)
    return restaurants


@app.route('/say_hello')  # Python 內建的裝飾詞，讓Flask監聽此URL 並return 返還結果
def hello_world():
    return 'Hello, World!'

@app.route('/')
def index():
    # 1. 動態取得所有類型
    all_types = get_all_types()
    return render_template('index.html', all_types=all_types)

@app.route('/filter', methods=['POST'])
def filter_restaurants():
    data = request.json  # 接收前端傳來的 JSON 資料
    selected_types = data.get('types', [])

    restaurants = []
    if selected_types:
        selected_restaurants = get_restaurants(selected_types)
        k = min(3, len(selected_restaurants))
        restaurants = random.sample(selected_restaurants, k)
    
    return jsonify(restaurants) # 以 JSON 格式回傳餐廳清單


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True, # 檔案更新網頁也會跟著更新
        port=5000
    )