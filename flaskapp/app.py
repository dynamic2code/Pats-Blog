from flask import Flask
from flask import render_template, request, redirect,flash,url_for, jsonify
from datetime import datetime

import requests
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/admin')
def admin():
    return render_template('admin.html')

# global variables
likes = 0
is_liked = False
dislikes = 0
is_disliked = False
blog_id = 0

# Function to check if the provided credentials are valid
def is_valid_credentials(name, email, password):
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()

    # Query the database to find a user with the provided name, email, and password
    cursor.execute("SELECT * FROM admin WHERE name = ? AND email = ? AND password = ?", (name, email, password))
    user = cursor.fetchone()

    conn.close()

    # If the user exists (non-empty result from the query), credentials are valid
    return user is not None

# Login route
@app.route('/admin/addBlog', methods=['POST'])
def addBlog():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Check if the provided credentials are valid
    if is_valid_credentials(name, email, password):
        # Redirect to the addBlog.html page or any other desired route
        return render_template('addBlog.html')
    else:
        # Redirect back to the login page with an error message
        return "Invalid Credentials. Please try again."

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
        flash('Error occurred while saving the blog.', 'error')

    return render_template('addBlog.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def userView():  
    global blog_id
    # Connect to the database
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM blogs ORDER BY id DESC LIMIT 1;")
    last_id_b = cursor.fetchall()
    blog_id = last_id_b[0][0]


    cursor.execute("SELECT blog FROM blogs WHERE id = ?", (blog_id,))
    latest = cursor.fetchall()
    latest_blog = latest[0][0]
    
    cursor.execute("SELECT title FROM blogs WHERE id < ? ORDER BY id DESC LIMIT 10;", (blog_id,))
    titles_b= cursor.fetchall()
    titles = [title[0] for title in titles_b if title[0] is not None]
    
    cursor.execute("SELECT comments FROM blogs WHERE id = ?", (blog_id,))
    comments_n = cursor.fetchall()
    comments_n = comments_n[0][0]
    
    cursor.execute("SELECT hearts FROM blogs WHERE id = ?", (blog_id,))
    hearts_n = cursor.fetchall()
    likes = hearts_n[0][0]
    
    cursor.execute("SELECT dislike FROM blogs WHERE id = ?", (blog_id,))
    dislike_n = cursor.fetchall()
    dislike = dislike_n[0][0]
    
    cursor.execute("SELECT name, comment FROM comments WHERE blog_id = ?", (blog_id,))
    comments_data = cursor.fetchall()
    comments = [comment[1] for comment in comments_data if comment[1] is not None]
    names = [comment[0] for comment in comments_data if comment[0] is not None]
    
    cursor.close()
    conn.close()

    return render_template('userView.html', blog= latest_blog, titles= titles, comments_n = comments_n, hearts = likes, dislike= dislike, comments= comments, names = names, last_id = blog_id)

@app.route('/search', methods=['GET', 'POST'])
def search():
    global blog_id
    try:
        if request.method == 'GET':
            # Get the title from the query parameters for a GET request
            title = request.args.get('name')
        elif request.method == 'POST':
            # Get the title from the submitted form for a POST request
            title = request.form['name']

        conn = sqlite3.connect('blogs.db')
        cursor = conn.cursor()

        # Use a SQL query to search for the blog with the given title
        search_blog = "SELECT blog FROM blogs WHERE title = ?"
        cursor.execute(search_blog, (title,))
        blog_n = cursor.fetchall()  # Assuming the query will return only one row for the blog
        blog = blog_n[0][0]

        # getting the blogs id
        cursor.execute("SELECT id FROM blogs WHERE title = ?", (title,))
        id_b = cursor.fetchall()
        blog_id = id_b[0][0]

        # getting the titles of ten blogs
        cursor.execute("SELECT title FROM blogs WHERE id < ? ORDER BY id DESC LIMIT 10;", (blog_id,))
        titles_b = cursor.fetchall()
        titles = [title[0] for title in titles_b if title[0] is not None]

        cursor.execute("SELECT comments FROM blogs WHERE id = ?", (blog_id,))
        comments_n = cursor.fetchall()
        comments_n = comments_n[0][0]

        cursor.execute("SELECT hearts FROM blogs WHERE id = ?", (blog_id,))
        hearts_n = cursor.fetchall()
        likes = hearts_n[0][0]

        cursor.execute("SELECT dislike FROM blogs WHERE id = ?", (blog_id,))
        dislike_n = cursor.fetchall()
        dislike = dislike_n[0][0]

        cursor.execute("SELECT name, comment FROM comments WHERE blog_id = ?", (blog_id,))
        comments_data = cursor.fetchall()
        comments = [comment[1] for comment in comments_data if comment[1] is not None]
        names = [comment[0] for comment in comments_data if comment[0] is not None]

        cursor.close()
        conn.close()

        return render_template('userView.html', blog=blog, titles=titles, comments_n=comments_n, hearts=likes, dislike=dislike, comments=comments, names = names, last_id=blog_id)

    except Exception as e:
        # Handle the error as per your requirement
        # For example, you can redirect the user to an error page or show a user-friendly message
        return render_template('error.html', error_message=str(e))

@app.route('/add_comment',methods=['GET', 'POST'] )
def add_comment():
    try:
        # Connect to the database
        connection = sqlite3.connect('blogs.db')
        cursor = connection.cursor()

        # Retrieve values from the form
        id = request.form['blog_id']
        name = request.form['name']
        comment = request.form['comment']

        # SQL query to insert the comment into the comments table
        cursor.execute("INSERT INTO comments (blog_id,name, comment) VALUES (?, ?, ?)", (id, name, comment))
        cursor.execute("UPDATE blogs SET comments = comments + 1 WHERE id = ?", (id,))
        # Commit the changes and close the database connection
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('userView'))

    except Exception as e:
        return redirect(url_for('error'))
    


@app.route('/mail_list',methods=['GET', 'POST'])
def mail_list():
    try:
        name = request.form['name']
        email = request.form['email']

        connection = sqlite3.connect('blogs.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO maillist (name, email) VALUES (?, ?)", (name, email))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('userView'))
    except:
        return redirect(url_for('error'))
    
@app.route('/like', methods=['POST'])
def like():
    global likes, is_liked, blog_id
    if not is_liked:
        connection = sqlite3.connect('blogs.db')
        cursor = connection.cursor()
        print(blog_id)
        cursor.execute("UPDATE blogs SET hearts = hearts + 1 WHERE id = ?", (blog_id,))
        connection.commit()
        
        is_liked = True

        # Return the updated like count (optional)
        cursor.execute("SELECT hearts FROM blogs WHERE id = ?", (blog_id,))
        hearts_n = cursor.fetchone()
        likes = hearts_n[0][0]  # Get the value of the first column of the first row
        cursor.close()
        connection.close()

    return jsonify({'likes': likes})

@app.route('/unlike', methods=['DELETE'])
def unlike():
    global likes, is_liked, blog_id
    if is_liked:
        connection = sqlite3.connect('blogs.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE blogs SET hearts = hearts - 1 WHERE id = ?", (blog_id,))
        connection.commit()

        is_liked = False
        # Return the updated like count (optional)
        cursor.execute("SELECT hearts FROM blogs WHERE id = ?", (blog_id,))
        like_n = cursor.fetchone()
        likes = like_n[0][0]  
        cursor.close()
        connection.close()
        
    return jsonify({'likes': likes})

@app.route('/dislike', methods=['POST'])
def dislike():
    global dislikes, is_disliked
    if not is_disliked:
        dislikes += 1
        is_disliked = True
    return jsonify({'dislikes': dislikes})

@app.route('/undislike', methods=['DELETE'])
def undislike():
    global dislikes, is_disliked
    if is_disliked:
        dislikes -= 1
        is_disliked = False
    return jsonify({'dislikes': dislikes})


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)