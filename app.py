from user import User, db_user, login
from article import Article, db
from flask import Flask, render_template, request, redirect
from flask_login import login_required, login_user, current_user
from flask_login import logout_user

app = Flask(__name__)
login.init_app(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db_user.init_app(app)
db.init_app(app)


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
