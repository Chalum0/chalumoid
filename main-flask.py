import flask
from flask import Flask, request, render_template, url_for, session, redirect, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from sqlCommands import *
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "masuperclef"
alphabet = [chr(i) for i in range(ord('a'),ord('z')+1)] + ["_", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

def get_db_connection():
    conn = sqlite3.connect('files/server-files/user.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute(innitDataBase)
    conn.commit()
    conn.close()

def convert_string(input_string):
    output_string = input_string.replace('_', ' ').title()
    return output_string

@app.route("/", methods=["GET"])
def form():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", button1="", button2=username, button1link="", button2link="/logout")
    return render_template("index.html", button1="Sign in", button2="Sign up", button1link="/signin", button2link="/signup")

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        password_hash = generate_password_hash(password)
        if password != password2:
            return "Passwords are not similar"

        for char in username:
            if char not in alphabet:
                return 'Username must only contain letter, number or "_"'


        conn = get_db_connection()
        try:
            conn.execute(NewUserInDB, (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            return 'Username already exists.'
        finally:
            conn.close()

        return redirect(url_for('login'))
    return render_template('signUp.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True  # This makes the session persistent
            return redirect("/")

        return 'Invalid username or password.'
    return render_template('login.html')


@app.route("/projects/bazaar-tracker/items/<item>")
def show_item_page(item):
    if "username" in session:
        username = session["username"]
        return render_template("item-page.html", button1="", button2=username, button1link="", button2link="/logout", item=convert_string(item))
    return render_template("item-page.html", button1="Sign in", button2="Sign up", button1link="/signin", button2link="/signup", item=convert_string(item))


@app.route("/projects/bazaar-tracker/items/<item>/api")
def item_api_page(item):
    with open('files/server-files/save.json', 'r') as f:
        item_data = json.load(f)
    print(item)
    print(item_data.keys())
    try:
        return jsonify(item_data[item])
    except KeyError:
        abort(404)


@app.route("/projects")
def projects():
    if "username" in session:
        username = session["username"]
        return render_template("projects.html", button1="", button2=username, button1link="", button2link="/logout")
    return render_template("projects.html", button1="Sign in", button2="Sign up", button1link="/signin", button2link="/signup")

@app.route("/projects/bazaar-tracker")
def bazaar_tracker():
    if "username" in session:
        username = session["username"]
        return render_template("bazaar-index.html", button1="", button2=username, button1link="", button2link="/logout")
    return render_template("bazaar-index.html", button1="Sign in", button2="Sign up", button1link="/signin", button2link="/signup")


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
