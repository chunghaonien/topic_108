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
        sql = "SELECT * FROM user WHERE account = %s AND password = %s"
        val = (account, password)

        cursor.execute(sql, val)
        result = cursor.fetchall()
        if result:
            return "True"
        else:
            return "False"
    finally:
        db.close()