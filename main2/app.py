from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL資料庫連線設定
app.config['MYSQL_HOST'] = 'localhost'  # MySQL伺服器位址
app.config['MYSQL_USER'] = 'username'  # MySQL使用者名稱
app.config['MYSQL_PASSWORD'] = 'password'  # MySQL使用者密碼
app.config['MYSQL_DB'] = 'database_name'  # MySQL資料庫名稱

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and user[2] == password:
        # 登入成功
        return redirect(url_for('dashboard'))
    else:
        # 登入失敗，顯示錯誤訊息
        error = '登入失敗，請檢查您的帳號和密碼！'
        return render_template('index.html', error=error)

@app.route('/dashboard')
def dashboard():
    return '歡迎進入儀表板！'

if __name__ == '__main__':
    app.run()
