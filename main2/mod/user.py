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
            return True
        else:
            return False
    finally:
        db.close()

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

def get_user_data(account, password):
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

        user_data = []
        for row in result:
            user = {
                'id': row[0],
                'account': row[1],
                'password': row[2],
                'username': row[3],
                'email': row[4],
                'birthday': row[5]
            }
            user_data.append(user)
        
        return user_data
    finally:
        db.close()