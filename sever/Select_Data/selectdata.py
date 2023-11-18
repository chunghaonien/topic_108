import mysql.connector

def select_user_id(user_id):
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
        sql = "SELECT * FROM scraping WHERE user_id = %"
        val = (user_id)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        # 
        if result[0] == user_id:
            return result
        else:
            # 如果使用者名稱不存在，回傳 "False"
            return ["False", None]
    except Exception as e:
        # 處理例外狀況，例如資料庫連接問題
        print(f"Error: {e}")
        return ["Error", None]
    finally:
        db.close()
