import mysql.connector
from datetime import datetime

def upload_scrape_data(user_id, scraped_data):
    try:
        db = mysql.connector.connect(
            host="140.131.114.242",
            port="3306",
            user="admin112510",
            password="@aA0937404883",
            database="112-webpy"
        )

        cursor = db.cursor()

        scrape_time = datetime.now().strftime("%Y-%m-%d")

        # 插入資料的 SQL 指令
        sql = "INSERT INTO scraping (user_id, scrap_time, scrap_data) VALUES (%s, %s, %s)"
        val = (user_id, scrape_time, scraped_data)

        try:
        # 執行插入資料的指令
            cursor.execute(sql, val)
        # 提交變更
            db.commit()
        except mysql.connector.Error as err:
        # 錯誤處理
            print(f"錯誤：{err}")

    except Exception as e:
        # 處理例外狀況，例如資料庫連接問題
        print(f"Error: {e}")
        return ["Error", None]
    finally:
        db.close()
        cursor.close()