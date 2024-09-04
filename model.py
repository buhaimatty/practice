import uuid
from flask import redirect, flash, url_for, session
from configparser import ConfigParser
import psycopg2

def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def connect():
    params = config()
    conn = psycopg2.connect(**params)
    return conn


def register_user(id, username, email, password):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.users (id, username, email, password)
                VALUES (%s, %s, %s, %s)
            """, (id, username, email, password))
            conn.commit()

            # print(f"User registered successfully with ID {id}.")
    except Exception as error:
        print(f"Error registering user: {error}")
    finally:
        conn.close()


def user_exists(email):
    conn = connect()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM public.users WHERE email = %s;"
            cur.execute(query, (email,))
            user = cur.fetchone()
            return user  # Returns the user record if found, otherwise None
    except Exception as error:
        print(f"Error: {error}")
        return None
    finally:
        conn.close()


def login_user(email, password, remember_me=False):
    user = user_exists(email)
    
    if user:
        stored_password = user[3]  # the password is in the 4th column
        if stored_password == password:

            # kepp log in
            session['user_id'] = user[0]  # store the user ID in session
            session['username'] = user[1]  # store the username in session
            session['is_admin'] = user[4]  # store the admin status in session
            session['logged_in'] = True

            if remember_me:
                session.permanent = True  # keep the session for 30 days
            else:
                session.permanent = False  # session expires when the browser closes

            return True
        else:
            flash("Invalid password")
            return False
    else:
        flash("User with this email does not exist")
        # return redirect(url_for('login'))
        return False;


def get_user_files(owner_id):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT file_name, created_at
                FROM public.files
                WHERE owner_id = %s
                ORDER BY created_at DESC
            """, (owner_id,))
            files = cur.fetchall()
            return files
    except Exception as error:
        print(f"Error fetching user files: {error}")
        return []
    finally:
        conn.close()


def add_file(file_name, owner_id, created_at):
    conn = connect()
    try:
        with conn.cursor() as cur:
            file_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO public.files (file_id, file_name, owner_id, created_at)
                VALUES (%s, %s, %s, %s)
            """, (file_id, file_name, owner_id, created_at))
            conn.commit()
            print(f"File added with ID {file_id}.")
    except Exception as error:
        print(f"Error adding file: {error}")
    finally:
        conn.close()


def is_admin(user_id):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT is_admin
                FROM public.users
                WHERE id = %s
            """, (user_id,))
            result = cur.fetchone()
            return result[0] if result else False
    except Exception as error:
        print(f"Error checking admin status: {error}")
        return False
    finally:
        conn.close()

