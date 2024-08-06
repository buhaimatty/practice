import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", 
                        password="12345", port=5432)

cur = conn.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS person (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        age INT        
    );
""")

conn.commit()

cur.close()
conn.close()
