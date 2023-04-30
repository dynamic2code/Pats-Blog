from flask import Flask
import requests
import sqlite3

app = Flask(__name__)
def auth():
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
                return True
        else:
            cursor.close()
            conn.close()
            return "The email you entered is incorect"
    else:
        cursor.close()
        conn.close()
        return "There are no registered name same as the name you enterd"



@app.route('/admin')
def admin():
    return 'Hello, World!'

@app.route('/')
def userView():
    
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()