from flask import Flask, session, abort, render_template, request, redirect, url_for
from model import *
from datetime import datetime, timedelta
import uuid
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


# File upload directory
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# UPLOAD_FOLDER = 'path/to/upload/directory'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['SECRET_KEY'] = '12345'  # for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)


@app.route('/')
def index():
    return render_template("index.html")


@app.errorhandler(Exception)
def handle_all_errors(error):
    # status_code = getattr(error, 'code', 500)
    status_code = getattr(error, 'code')

    if 300 <= status_code < 400:
        return render_template('3xx.html', error_code=status_code), status_code
    elif 400 <= status_code < 500:
        return render_template('4xx.html', error_code=status_code), status_code
    elif 500 <= status_code < 600:
        return render_template('5xx.html', error_code=status_code), status_code
    else:
        return render_template('error.html', error_code=status_code), status_code


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
        
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repeated_password = request.form.get('repeat_password')

        # VALIDATION PART
        # REGISTATION PART
        # ENCRYPTION OF PASSWORD ? PART

        # when everything is OK --> CREATE USER
        id = str(uuid.uuid1())
        register_user(id, username, email, password)
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            return redirect(url_for('success'))
        
        return render_template("login.html")
        
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        repeated_password = request.form.get('repeat_password')
        remember_me = request.form.get('remember_me') == 'on'  # Checkbox in form

        # VALIDATION PART ?
        # ENCRYPTION OF PASSWORD ? PART

        user = login_user(email, password, remember_me) # verify user
        if(user):
            return redirect(url_for('success'))
        return render_template("login.html")  # Stay on login page if login fails


@app.route('/logout')
def logout():
    session.clear()  # clear all session data
    return redirect(url_for('login'))  # redirect back to the login page


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template("success.html");


@app.route('/user_index', methods=['GET', 'POST'])
def user_index():
    owner_id = session.get('user_id')
    if owner_id:
        files_arr = get_user_files(owner_id)
        return render_template("userIndex.html", files=files_arr)
    else:
        return redirect(url_for('login'))


@app.route('/upload_file', methods=['POST'])
def upload_file():
    owner_id = session.get('user_id')
    if owner_id:
        file = request.files['file']
        if file:
            file_name = file.filename
            created_at = datetime.now()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            add_file(file_name, owner_id, created_at)
            return redirect(url_for('user_index'))
    return redirect(url_for('login'))


# FOR TESTING
@app.route('/promote_to_admin', methods=['POST'])
def promote_to_admin():
    user_id = session.get('user_id')
    if user_id:
        conn = connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE public.users
                    SET is_admin = TRUE
                    WHERE id = %s
                """, (user_id,))
                conn.commit()
                print(f"User {user_id} promoted to admin.")
        except Exception as error:
            print(f"Error promoting user to admin: {error}")
        finally:
            conn.close()
        return redirect(url_for('success'))  # redirect back to page
    return redirect(url_for('login'))


@app.route('/header_test', methods=['GET', 'POST'])
def header_test():
    # username = session.get('username')
    return render_template('header.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

