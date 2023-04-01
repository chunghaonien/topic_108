import mysql.connector

def into_mysql(url, date):
    try:
        db = mysql.connector.connect(
        host="140.131.114.242",
        port="3306",
        user="admin112510",
        password="@aA0937404883",
        database="112-webpy"
        )

        cursor = db.cursor()
        sql = "INSERT INTO testforflask (url, content) VALUES (%s, %s, %s)"
        val = (url, date)

        cursor.execute(sql, val)

        db.commit()
        return '儲存成功'
    except:
        return '儲存失敗'
