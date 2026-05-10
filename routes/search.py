from flask import Blueprint, render_template, request, abort, redirect
from flask_login import current_user
from sqlalchemy import func
import bleach

from models import db_session
from models.products import Products
from models.users import User

from forms.product import AddProductForm

allowed_tags = {'abbr', 'ul', 'em', 'li', 'i', 'strong', 'ol', 'acronym', 'code', 'blockquote', 'b', 'a',
                'u', 'h1', 'h2', 'h3', 'p'}

# Создаем чертеж
search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    per_page = 35
    query = request.args.get('q')
    order_by = request.args.get('ord')
    seller = request.args.get('seller', type=int, default=0)
    page = int(request.args.get('page') or 1)
    db_sess = db_session.create_session()
    items = db_sess.query(Products).filter((
        Products.title.ilike(f'%{query}%') |
        Products.tags.ilike(f'%{query}%'.lower())) &
        ((Products.user_id == seller) | (seller == 0) ))
    if order_by == "lp":
        items = items.order_by(Products.price)
    elif order_by == "gp":
        items = items.order_by(Products.price.desc())
    elif order_by == "sd":
        items = items.order_by(Products.bought.desc())
    elif order_by == "ctr":
        items = items.order_by((Products.clicked / Products.showed).desc())

    items = items.limit(per_page).offset((page - 1) * per_page).all()

    for i in items:
        i.showed += 1
    db_sess.commit()

    results_num = len(items)
    return render_template(
                        'feed.html',
                        title=query,
                        num=results_num,
                        items=items,
                        include=render_template("search.html")
                    )
