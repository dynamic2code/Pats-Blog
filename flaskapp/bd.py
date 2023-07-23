# creates the db for the whole app
import sqlite3

def create_db_tables():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect("blogs.db")
    cursor = conn.cursor()

    # Create the 'admin' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )''')

    # Create the 'blogs' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS blogs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        blog TEXT NOT NULL,
                        title TEXT NOT NULL,
                        comments INTEGER DEFAULT 0,
                        hearts INTEGER DEFAULT 0,
                        dislike INTEGER DEFAULT 0
                    )''')

    # Create the 'comments' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                        count INTEGER PRIMARY KEY AUTOINCREMENT,
                        blog_id INTEGER NOT NULL,
                        comment TEXT NOT NULL,
                        FOREIGN KEY (blog_id) REFERENCES blogs(id)
                    )''')

    # Create the 'maillist' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS maillist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE
                    )''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db_tables()
    print("Database tables created successfully.")