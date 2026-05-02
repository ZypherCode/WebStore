from flask import Blueprint, render_template, abort, redirect
from flask_login import current_user
import bleach

from models import db_session
from models.products import Products
from models.reviews import Review
from models.carts import Cart

from forms.product import AddProductForm
from forms.review import AddReviewForm
from forms.delete_item import DeleteItemForm

allowed_tags = {'abbr', 'ul', 'em', 'li', 'i', 'strong', 'ol', 'acronym', 'code', 'blockquote', 'b', 'a',
                'u', 'h1', 'h2', 'h3', 'p'}

# Создаем чертеж
product_bp = Blueprint('product', __name__)


@product_bp.route('/product/<query_id>', methods=['GET', 'POST'])
def product_page(query_id):
    db_sess = db_session.create_session()
    
    item = db_sess.query(Products).filter(Products.id == int(query_id)).first()
    if not item:
        return render_template("error.html", title="Товар не найден", 
                           error={"type": "Товар не найден", "text": "Возможно, он был удален."})
    
    item.clicked += 1
    if not current_user.is_authenticated:
        return render_template('product.html', title=item.title, item=item, seller=item.user, form=None, has_review=True, in_cart=False)
    
    my_review = db_sess.query(Review).filter(Review.product_id == query_id, Review.user == current_user).first() != None
    
    form = AddReviewForm()
    if form.validate_on_submit():
        if my_review:
            return render_template('product.html', title=item.title, item=item, seller=item.user, form=form)

        voice = form.voice.data == "good"
        item.good_marks += voice
        item.bad_marks += not voice
        review = Review(user_id=current_user.id, product_id=query_id, 
                        content=form.content.data, good=voice)
        db_sess.add(review)
        db_sess.commit()
        return redirect(f"/product/{query_id}")
    
    db_sess.commit()

    in_cart = db_sess.query(Cart).filter(Cart.user == current_user, Cart.product == item).first() != None
    return render_template('product.html', title=item.title, item=item, seller=item.user, form=form, has_review=my_review, in_cart=in_cart)


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
                           price=form.price.data, stock=form.stock.data, user_id=current_user.id)
        db_sess.add(product)
        db_sess.commit()

        return redirect(f"/product/{product.id}")

    return render_template('add_product.html', title="Новый товар", form=form)

@product_bp.route('/seller/product/<query_id>')
def product_info_page(query_id):
    if not current_user.is_authenticated:
        abort(401)

    if not current_user.is_seller:
        abort(403)

    db_sess = db_session.create_session()
    
    product = db_sess.query(Products).filter(Products.id == int(query_id)).first()
    if not product:
        return render_template("error.html", title="Товар не найден", 
                           error={"type": "Товар не найден", "text": "Возможно, он был удален."})
    
    if product.user_id != current_user.id:
        abort(403)

    return render_template("product-info.html", title=f"Аналитика | {product.title}", product=product)

@product_bp.route('/product/<query_id>/delete', methods=['GET', 'POST'])
def delete_product(query_id):
    if not current_user.is_authenticated:
        abort(401)

    if not current_user.is_seller:
        abort(403)

    db_sess = db_session.create_session()
    
    product = db_sess.query(Products).filter(Products.id == int(query_id)).first()
    if not product:
        return render_template("error.html", title="Товар не найден", 
                           error={"type": "Товар не найден", "text": "Возможно, он был удален."})
    
    if product.user_id != current_user.id:
        abort(403)

    form = DeleteItemForm()
    if form.validate_on_submit():
        db_sess.delete(product)
        db_sess.commit()
        return redirect("/seller/dashboard")

    return render_template("delete-item.html", title="Удаление товара", form=form)