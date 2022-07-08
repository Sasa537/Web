from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, current_user
from flask_login import UserMixin, logout_user

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# класс модели
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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    password_hash = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.id

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


@app.route('/')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("index.html", article=articles, status=current_user.is_authenticated)


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            if title and intro and text:
                db.session.add(article)
                db.session.commit()
                return redirect('/')

            else:
                return redirect('/add')

        except:
            return "Error adding"

    else:
        return render_template("add.html")


@app.route('/posts/<int:id>')
def posts(id):
    article = Article.query.get(id)
    return render_template("posts.html", art=article, status=current_user.is_authenticated)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        article = Article.query.get(id)
        return render_template("update.html", art=article)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
