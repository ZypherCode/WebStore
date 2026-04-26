from flask import Blueprint, request, render_template, abort
from flask_login import current_user

from models import db_session
from models.users import User
from models.carts import Cart


# Создаем чертеж
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
def html_cart():
    return render_template("cart.html")

@cart_bp.route('/cart/json', methods=['GET'])
def get_cart():
    if not current_user.is_authenticated:
        return abort(401)
    
    return {"items": [
        {"img": i.product.image, "title": i.product.title, "link": f"/product/{i.product.id}",
         "price": i.product.price, "quantity": i.quantity, "id": i.id} for i in current_user.carts
    ]}

@cart_bp.route('/cart', methods=['POST'])
def edit_cart():
    if not current_user.is_authenticated:
        return abort(403)
    
    db_sess = db_session.create_session()
    
    if request.json["op"] == "del":
        item = db_sess.query(Cart).filter(Cart.user == current_user, Cart.id == request.json["id"]).first()
        if item:
            db_sess.delete(item)
            db_sess.commit()
            return {"succes": True}
        else:
            return {"succes": False}
    
    elif request.json["op"] == "add":
        item = db_sess.query(Cart).filter(Cart.user == current_user, Cart.product_id == request.json["id"]).first()
        if not item:
            
            cart = Cart(user_id=current_user.id, product_id=request.json["id"], quantity=request.json["q"])
            db_sess.add(cart)
        else:
            item.quantity += request.json["q"]

        db_sess.commit()
        return {"succes": True}

    return abort(400)