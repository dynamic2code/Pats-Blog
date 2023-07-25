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
        print("Error:", e)
        flash('Error occurred while saving the blog.', 'error')

    return render_template('addBlog.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/')
def userView():  
    # Connect to the database
    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM blogs ORDER BY id DESC LIMIT 1;")
    last_id_b = cursor.fetchall()
    last_id = last_id_b[0][0]
    print ("last id",last_id)

    cursor.execute("SELECT blog FROM blogs WHERE id = ?", (last_id,))
    latest = cursor.fetchall()
    latest_blog = latest[0][0]
    
    cursor.execute("SELECT title FROM blogs WHERE id < ? ORDER BY id DESC LIMIT 10;", (last_id,))
    titles_b= cursor.fetchall()
    titles = [title[0] for title in titles_b if title[0] is not None]
    
    cursor.execute("SELECT comments FROM blogs WHERE id = ?", (last_id,))
    comments_n = cursor.fetchall()
    comments_n = comments_n[0][0]
    
    cursor.execute("SELECT hearts FROM blogs WHERE id = ?", (last_id,))
    hearts_n = cursor.fetchall()
    hearts = hearts_n[0][0]
    
    cursor.execute("SELECT dislike FROM blogs WHERE id = ?", (last_id,))
    dislike_n = cursor.fetchall()
    dislike = dislike_n[0][0]
    
    cursor.execute("SELECT comment FROM comments WHERE blog_id = ?", (last_id,))
    comments_b = cursor.fetchall()
    comments = [comment[0] for comment in comments_b if comment[0] is not None]
    

   

    print(titles)
    cursor.close()
    conn.close()

    

    return render_template('userView.html', blog= latest_blog, titles= titles, comments_n = comments_n, hearts = hearts, dislike= dislike, comments= comments, last_id = last_id)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        # Get the title from the query parameters for a GET request
        title = request.args.get('name')
    elif request.method == 'POST':
        # Get the title from the submitted form for a POST request
        title = request.form['name']

    conn = sqlite3.connect('blogs.db')
    cursor = conn.cursor()
    
    # Use a SQL query to search for the blog with the given title
    search_blog = f"SELECT blog FROM blogs WHERE title = ?"
    cursor.execute(search_blog, (title,))
    blog_n = cursor.fetchall()  # Assuming the query will return only one row for the blog
    blog = blog_n[0][0]

    # getting the blogs id
    cursor.execute("SELECT id FROM blogs WHERE title = ?", (title,))
    id_b = cursor.fetchall()
    id = id_b[0][0]

    # getting the titles of ten blogs
    cursor.execute("SELECT title FROM blogs WHERE id < ? ORDER BY id DESC LIMIT 10;", (id,))
    titles_b= cursor.fetchall()
    titles = [title[0] for title in titles_b if title[0] is not None]

    cursor.execute("SELECT comments FROM blogs WHERE id = ?", (id,))
    comments_n = cursor.fetchall()
    comments_n = comments_n[0][0]

    cursor.execute("SELECT hearts FROM blogs WHERE id = ?", (id,))
    hearts_n = cursor.fetchall()
    hearts = hearts_n[0][0]
    
    cursor.execute("SELECT dislike FROM blogs WHERE id = ?", (id,))
    dislike_n = cursor.fetchall()
    dislike = dislike_n[0][0]
    
    cursor.execute("SELECT comment FROM comments WHERE blog_id = ?", (id,))
    comments_b = cursor.fetchall()
    comments = [comment[0] for comment in comments_b if comment[0] is not None]

    # cursor.execute("SELECT name FROM comments WHERE blog_id = ?", (id,))
    # name = cursor.fetchall()
    # name = name



    cursor.close()
    conn.close()

    return render_template('userView.html', blog=blog, titles= titles, comments_n = comments_n, hearts = hearts, dislike= dislike, comments= comments, last_id = id)


@app.route('/add_comment',methods=['GET', 'POST'] )
def add_comment():
    try:
        # Connect to the database
        connection = sqlite3.connect('blogs.db')
        cursor = connection.cursor()

        # Retrieve values from the form
        id = request.form['blog_id']
        comment = request.form['comment']

        # SQL query to insert the comment into the comments table
        cursor.execute("INSERT INTO comments (blog_id, comment) VALUES (?, ?)", (id, comment))
        cursor.execute("UPDATE blogs SET comments = comments + 1;")
        # Commit the changes and close the database connection
        connection.commit()

        
        cursor.close()
        connection.close()

        return redirect(url_for('userView'))

    except Exception as e:
        return redirect(url_for('error'))
    
@app.route('/like_blog', methods=['POST'])
def like_blog():
    blog_id = request.form.get('blog_id')  # Get the blog ID from the request
    user_ip = request.remote_addr  # Get the user's IP address (for demonstration purposes)
    liked_users = likes_data.get(blog_id, {}).get('liked_users', set())

    if user_ip not in liked_users:
        # Increment like count and mark user as liked
        likes_data[blog_id] = {
            "likes": likes_data.get(blog_id, {}).get('likes', 0) + 1,
            "liked_users": liked_users | {user_ip}
        }
    else:
        # Decrement like count and remove user's like status
        likes_data[blog_id] = {
            "likes": likes_data.get(blog_id, {}).get('likes', 0) - 1,
            "liked_users": liked_users - {user_ip}
        }

    return jsonify({"likes": likes_data.get(blog_id, {}).get('likes', 0)})


@app.route('/mail_list',methods=['GET', 'POST'])
def mail_list():
    try:
        return redirect(url_for('userView'))
    except:
        return redirect(url_for('error'))
    


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)