from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add')
def add():
        return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)