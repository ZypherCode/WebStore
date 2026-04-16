from flask import Flask, render_template
from config import Consts
from flask_login import LoginManager

from models import db_session
from models.users import User

from forms.user import RegisterForm

from routes.auth import main_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = Consts.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)


app.register_blueprint(main_bp)

@app.route("/")
def index():
    return render_template("base.html")

def main():
    db_session.global_init("db/store.db")
    app.run()


if __name__ == '__main__':
    main()
