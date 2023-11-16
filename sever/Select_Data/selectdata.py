import mysql.connector

def select_user_id(username):
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
        sql = "SELECT user_id FROM user WHERE username = %s"
        val = (username,)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        # 如果使用者名稱存在，回傳使用者名稱和對應的 user_id
        if result:
            user_id = result[0]
            return ["True", user_id]
        else:
            # 如果使用者名稱不存在，回傳 "False"
            return ["False", None]
    except Exception as e:
        # 處理例外狀況，例如資料庫連接問題
        print(f"Error: {e}")
        return ["Error", None]
    finally:
        db.close()
