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
        sql = "SELECT * FROM scraping WHERE user_id = %s"
        val = (user_id)
        cursor.execute(sql, val)
        results = cursor.fetchall()  # 获取所有符合条件的行

        # 
        if results[0] == user_id:
            return results
        else:
            # 如果结果为空，回傳 ["False", None]
            return ["False", None]
    except Exception as e:
        # 處理例外狀況，例如資料庫連接問題
        print(f"Error: {e}")
        return ["Error", None]
    finally:
        db.close()
