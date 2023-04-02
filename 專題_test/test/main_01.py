# 引入必要的套件
from flask import Flask, render_template, request
import mysql.connector

# 建立 Flask 應用程式
app = Flask(__name__)

# 路由設定，將 / 指向 HTML 頁面
@app.route('/')
def index():
    return render_template('test1.html')

# 處理表單提交的 POST 請求
@app.route('/submit', methods=['POST'])
def submit():
    # 獲取表單數據
    url = request.form['user_url']
    user_id = request.form['user_id']
    content = request.form['content']


    # 建立與 MySQL 的連接
    conn = mysql.connector.connect(
        user='admin112510',
        password='@aA0937404883',
        host='140.131.114.242:3306',
        database='112-webpy'
    )

    # 建立 cursor 物件
    cursor = conn.cursor()

    # 執行 INSERT 敘述，將數據插入資料庫
    cursor.execute("INSERT INTO messages (url, user_id, content) VALUES (%s, %s, %s)", (url, user_id, content))

    # 提交變更
    conn.commit()

    # 關閉 cursor 和連接
    cursor.close()
    conn.close()


# 執行應用程式
if name == 'main':
    app.run(debug=True)