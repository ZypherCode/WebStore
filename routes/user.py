from flask import Blueprint, render_template, abort, redirect
from flask_login import current_user

from models import db_session
from models.users import User

from utils import format_number

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
        #return render_template("seller_guest.html", title=f"Продавец {user.name}", user=user)
        items = user.products
        boughts = 0
        good = 0
        bad = 0
        for i in items:
            i.showed += 1
            boughts += i.bought
            good += i.good_marks
            bad += i.bad_marks
        db_sess.commit()
        return render_template('feed.html', title=user.name, num=len(items), items=items, 
                               include=render_template("seller_guest.html", 
                                                       user=user, bought=format_number(boughts), mark=(good / (good + bad)) * 100))
    elif user.id == current_user.id:
        return redirect("/account")
    else:
        return abort(403)


@user_bp.route('/seller/dashboard')
def account_page():
    if not current_user.is_authenticated:
        abort(401)

    if not current_user.is_seller:
        abort(403)

    products = current_user.products
    total_showed = 0
    total_clicked = 0
    total_bought = 0
    revenue = 0

    for p in products:
        total_showed += p.showed
        total_clicked += p.clicked
        total_bought += p.bought
        revenue += p.bought * p.price

    ctr = (total_clicked / total_showed * 100) if total_showed else 0

    return render_template("dashboard.html", title="Пользователь", products=products,
                            stats={
                                "showed": total_showed,
                                "clicked": total_clicked,
                                "bought": total_bought,
                                "revenue": revenue,
                                "ctr": round(ctr, 2)
                            })