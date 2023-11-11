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
            username_sql = "SELECT username FROM user WHERE account = %s"
            cursor.execute(username_sql, (account,))
            username_result = cursor.fetchone()

            if username_result:
                # 如果使用者名稱存在，回傳 "True" 和使用者名稱
                return ["True,", username_result[0]]
            else:
                # 如果使用者名稱不存在，回傳 "False"
                return "False"
        else:
            # 如果帳號和密碼不匹配，回傳 "False"
            return "False"
    finally:
        db.close()
