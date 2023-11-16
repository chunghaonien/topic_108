import mysql.connector

def login(account, password):
    try:
        db = mysql.connector.connect(
            host="140.131.114.242",
            port="3306",
            user="admin112510",
            password="@aA0937404883",
            database="112-webpy"
        )

        cursor = db.cursor()

        # 檢查帳號和密碼的 SQL 語句
        sql = "SELECT * FROM user WHERE account = %s AND password = %s"
        val = (account, password)
        cursor.execute(sql, val)
        result = cursor.fetchall()

        # 如果帳號和密碼匹配，再從資料庫中獲取使用者名稱
        if result:
            user_sql = "SELECT username, user_id FROM user WHERE account = %s AND password = %s"
            cursor.execute(user_sql, (account, password))
            result_user = cursor.fetchall()

            if result_user:
                # 如果使用者名稱存在，回傳 "True" 和使用者名稱
                return "True", result_user
            else:
                # 如果使用者名稱不存在，回傳 "False"
                return "False"
        else:
            # 如果帳號和密碼不匹配，回傳 "False"
            return "False"
    finally:
        db.close()

response = str(login("123", "123"))

print(response)