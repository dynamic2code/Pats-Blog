from flask import Flask
from flask import render_template, request, redirect,flash,url_for
from datetime import datetime

import requests
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

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
            return "The email you entered is incorrect"
    else:
        cursor.close()
        conn.close()
        return "There are no registered name same as the name you entered"
    
@app.route('/admin/addBlog/saveBlog', methods=['POST'])
def saveBlog():
    date = datetime.now().date()
    blog = request.form['blog']
 
    # Connect to the database
    conn = sqlite3.connect('blogs.db')

    # Create a cursor object
    cursor = conn.cursor()

    print(blog)
    cursor.execute("INSERT INTO blogs (date, blog) VALUES (?, ?)", (date, blog))
    cursor.close()
    conn.close()

    flash('Blog saved successfully!', 'success')
    return render_template('addBlog.html')

@app.route('/')
def userView():
    # Connect to the database
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()
    latest_blog = f"SELECT * FROM blogs ORDER BY date DESC LIMIT 1;"
    cursor.execute(latest_blog)
    cursor.close()
    conn.close()

    return render_template('userView.html', blog= latest_blog)

@app.route('/search', methods=['GET', 'POST'])
def search():
    name = request.form['name']
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()
    search_blog = f""
    cursor.execute(search_blog)
    cursor.close()
    conn.close()

    return render_template('userView.html',blog = search_blog )

if __name__ == "__main__":
    # app.run()
    app.run(debug=True)