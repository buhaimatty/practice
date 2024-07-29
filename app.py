from flask import Flask, render_template
import psycopg2
from config import config

def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')


if __name__ == "__main__":
    connect()

# app = Flask(__name__)
# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     connect()
    # app.run(host="0.0.0.0", port=8080, debug=True)
