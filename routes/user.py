from flask import Blueprint, render_template, abort, redirect
from flask_login import current_user

from models import db_session
from models.users import User

# Создаем чертеж
user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<query_id>')
def user_page(query_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(query_id)).first()

    if not user:
        return render_template("error.html", title="Пользователь не найден", 
                           error={"type": "Пользователь не найден", "text": "Он не существует или был удален."})
    
    if user.is_seller:
        return render_template("error.html", title="Пользователь", 
                           error={"type": "Не реализовано", "text": "Подождите, пока разработчик допилит страницу."})
    elif user.id == current_user.id:
        return redirect("/account")
    else:
        return abort(403)


@user_bp.route('/account')
def account_page():
    return render_template("error.html", title="Пользователь", 
                           error={"type": "Не реализовано", "text": "Подождите, пока разработчик допилит страницу."})