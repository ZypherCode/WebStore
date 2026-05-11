from flask import Flask, render_template, request
from config import Consts
from flask_login import LoginManager, current_user

from models import db_session
from models.users import User
from models.products import Products
from models.carts import Cart

from forms.user import RegisterForm

from routes.auth import auth_bp
from routes.search import search_bp
from routes.cart import cart_bp
from routes.product import product_bp
from routes.user import user_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = Consts.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.__factory.remove()

app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)


@app.route("/")
def index():
    per_page = 50
    page = int(request.args.get('page') or 1)
    db_sess = db_session.create_session()
    items = db_sess.query(Products).order_by((Products.clicked / Products.showed).desc()) \
        .limit(per_page).offset((page - 1) * per_page).all()

    for i in items:
        i.showed += 1
    db_sess.commit()

    results_num = len(items)
    return render_template('feed.html', title="Главная", num=results_num, items=items, include="<h1>Топ-50<h1>")

def main():
    db_session.global_init("db/store.db")
    app.run(host="127.0.0.1", port="8080")


@app.errorhandler(403)
def handle_unexpected_error(e):
    text = "Вы не можете попасть на эту страницу."
    if not current_user.is_authenticated:
        text += " Возможно, вам стоит авторизироваться."
    return render_template("error.html", title="Ошибка", 
                           error={"type": "Заблокировано", "text": text})

if __name__ == '__main__':
    main()
