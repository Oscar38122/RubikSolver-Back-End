import mysql.connector

def resetFaces():
    db = mysql.connector.connect(
            host="localhost",
            port=3306,  
            user="root",
            password="root",
            database="rubiksolver"
        )
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE faces;")
    db.commit()