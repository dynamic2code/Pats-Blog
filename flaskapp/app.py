from flask import Flask
from flask import render_template, request, redirect

import requests
import sqlite3

app = Flask(__name__)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/addBlog', methods=['POST'])
def addBlog():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Connect to the database
    conn = sqlite3.connect('blogs.db')

    # Create a cursor object
    cursor = conn.cursor()
    query_name = f"SELECT * FROM admin WHERE name = '{name}'"
    query_email = f"SELECT * FROM admin WHERE email = '{email}'"
    query_pass = f"SELECT * FROM admin WHERE password = '{password}'"

    check_for_name =  cursor.execute(query_name)
    if (check_for_name):
        # where name 
        check_for_email = cursor.execute(query_email)
        if (check_for_email):
            # where email and name
            check_for_password = cursor.execute(query_pass)
            if check_for_password:
                cursor.close()
                conn.close()
                return render_template('addBlog.html')
        else:
            cursor.close()
            conn.close()
            return "The email you entered is incorect"
    else:
        cursor.close()
        conn.close()
        return "There are no registered name same as the name you enterd"


@app.route('/')
def userView():
    return render_template('userView.html')

if __name__ == "__main__":
    app.run()