from flask import Blueprint, render_template, abort, redirect
from flask_login import current_user
import bleach

from models import db_session
from models.products import Products

from forms.product import AddProductForm

allowed_tags = {'abbr', 'ul', 'em', 'li', 'i', 'strong', 'ol', 'acronym', 'code', 'blockquote', 'b', 'a',
                'u', 'h1', 'h2', 'h3', 'p'}

# Создаем чертеж
product_bp = Blueprint('product', __name__)


@product_bp.route('/product/<query_id>')
def product_page(query_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Products).filter(Products.id == int(query_id)).first()
    if not item:
        return render_template("error.html", title="Товар не найден", 
                           error={"type": "Товар не найден", "text": "Возможно, он был удален."})
    
    item.clicked += 1
    db_sess.commit()

    return render_template('product.html', title=item.title, item=item, seller=item.user)


@product_bp.route('/product/new', methods=['GET', 'POST'])
def new_product():
    if not current_user.is_authenticated:
        return abort(401)
    if not current_user.is_seller:
        return abort(403)

    form = AddProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = Products(title=form.title.data, content=bleach.clean(form.content.data, tags=allowed_tags),
                           tags=form.tags.data.lower(), image=form.image.data, 
                           price=form.price.data, user_id=current_user.id)
        db_sess.add(product)
        db_sess.commit()

        return redirect(f"/product/{product.id}")

    return render_template('add_product.html', title="Новый товар", form=form)