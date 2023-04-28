from flask import Flask

app = Flask(__name__)

@app.route('/admin')
def admin():
    return 'Hello, World!'

@app.route('/')
def userView():
    
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()