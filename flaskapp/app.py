from flask import Flask
from flask import render_template, request, redirect
import datetime

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
    
@app.route('/admin/addBlog/saveBlog', methods=['POST'])
def saveBlog():
    date = datetime.datetime.now()
    heading = request.form['heading']
    first_par = request.form['first_par']
    second_par = request.form['second_par']
    third_par = request.form['third_par']
    forth_par = request.form['forth_par']
    fivth_par = request.form['fivth_par']
    image1  = request.files['image1'].filename
    image2  = request.files['image2'].filename
    author = request.form['author']
    file_content = request.files['image1']
    file_content2 = request.files['image2']

    file_content.save("uploads/" + image1)
    file_content2.save("uploads/" + image2)
    # Connect to the database
    conn = sqlite3.connect('blogs.db')

    # Create a cursor object
    cursor = conn.cursor()

    query = f"INSERT INTO blogs '{date}', '{heading}', '{first_par}', '{second_par}', '{third_par}', '{forth_par}', '{fivth_par}' '{image1}', '{image2}', '{author}'"
    cursor.execute(query)
    cursor.close()
    conn.close()


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

@app.route('/search_results')
def search():
    pass

if __name__ == "__main__":
    app.run()