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
    title = request.form['title']
 
    try:
        # Connect to the database
        conn = sqlite3.connect('blogs.db')

        # Create a cursor object
        cursor = conn.cursor()

        cursor.execute("INSERT INTO blogs (date, blog, title) VALUES (?, ?, ?)", (date, blog, title))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Blog saved successfully!', 'success')

    except sqlite3.Error as e:
        # Handle the error, log it, or print it
        print("Error:", e)
        flash('Error occurred while saving the blog.', 'error')

    return render_template('addBlog.html')

@app.route('/')
def userView():
    # Connect to the database
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor() 
    cursor.execute("SELECT blog FROM blogs ORDER BY id DESC LIMIT 1;")
    latest = cursor.fetchall()
    latest_blog = latest[0][0]
    cursor.execute("SELECT title FROM blogs LIMIT 10;")
    titles_b= cursor.fetchall()
    titles = [title[0] for title in titles_b if title[0] is not None]
    print(titles)
    cursor.close()
    conn.close()

    

    return render_template('userView.html', blog= latest_blog, titles= titles)

@app.route('/search', methods=['GET', 'POST'])
def search():
    name = request.form['name']
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()
    search_blog = f""
    cursor.execute(search_blog)
    cursor.close()
    conn.close()

    return render_template('userView.html',blog = search_blog, )

if __name__ == "__main__":
    # app.run()
    app.run(debug=True)