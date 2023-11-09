import mysql.connector

def register(account, password, username):
    try:
        db = mysql.connector.connect(
            host="140.131.114.242",
            port="3306",
            user="admin112510",
            password="@aA0937404883",
            database="112-webpy"
        )

        cursor = db.cursor()
        sql = "INSERT INTO user (account, password, username) VALUES (%s, %s, %s)"
        val = (account, password, username)
        cursor.execute(sql, val)
        db.commit()


        return True
    except:

        return False