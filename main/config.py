from flask import Flask, render_template, request, redirect, url_for
import hashlib
import mysql.connector

app = Flask(__name__)

# 設置MySQL資料庫連接
db = mysql.connector.connect(
  host='140.131.114.242:3306',
   user='admin112510',
  password='@aA0937404883',
   database='112-webpy'
)

# 創建一個游標對象
cursor = db.cursor()

# 定義會員資料庫的表結構
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

# 將密碼進行SHA256加密
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 註冊新用戶
def register_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()

# 檢查用戶名和密碼是否匹配
def check_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
    user = cursor.fetchone()
    if user is not None:
        return True
    else:
        return False

# 設置首頁路由
@app.route('/')
def index():
    return render_template('index.html')

# 設置註冊路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

# 設置登入路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            return redirect(url_for('success', name=username))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html')

# 設置登入成功後的路由
@app.route('/success/<name>')
def success(name):
    return 'Login successful, welcome %s!' % name

if __name__ == '__main__':
    app.run(debug=True)
