import mysql.connector

db = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="1234"
)

cur = db.cursor()

cur.execute("show databases")

for i in cur:
    print(i)

db.commit()

cur.close()
db.close()
