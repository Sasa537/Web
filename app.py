from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, title, intro, text):
        self.title = title
        self.intro = intro
        self.text = text

    def __repr__(self):
         return '<Article %r>' % self.id


@app.route('/')
def index():
    articles = Article.query.order_by(Article.date).all()
    return render_template("index.html", article=articles)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
           db.session.add(article)
           db.session.commit
           return redirect('/')

        except:
            return "Error adding"

    else:
        return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
