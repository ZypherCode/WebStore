from flask import Blueprint, request, render_template, abort, redirect
from flask_login import current_user

from models import db_session
from models.users import User
from models.carts import Cart
from models.order import Order
from models.order_item import OrderItem

from forms.checkout import CheckoutForm


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
        return abort(401)
    
    db_sess = db_session.create_session()
    
    if request.json["op"] == "del":
        item = db_sess.query(Cart).filter(Cart.user == current_user, Cart.id == request.json["id"]).first()
        if item:
            db_sess.delete(item)
            db_sess.commit()
            return {"succes": True}
        else:
            return {"succes": False}
        
    elif request.json["op"] == "qnt":
        item = db_sess.query(Cart).filter(Cart.user == current_user, Cart.id == request.json["id"]).first()
        if item:
            item.quantity = request.json["q"]
            db_sess.commit()
            return {"succes": True}
        else:
            return {"succes": False}
    
    elif request.json["op"] == "add":
        item = db_sess.query(Cart).filter(Cart.user == current_user, Cart.product_id == request.json["id"]).first()
        if not item:
            
            cart = Cart(user_id=current_user.id, product_id=request.json["id"], quantity=request.json["q"])
            db_sess.add(cart)

        db_sess.commit()
        return {"succes": True}

    return abort(400)


@cart_bp.route('/checkout', methods=['GET', 'POST'])
def make_order():
    if not current_user.is_authenticated:
        return abort(401)
    
    if not current_user.carts:
        return redirect("/cart")
    
    form = CheckoutForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        order = Order(user_id=current_user.id, status=0)
        db_sess.add(order)
        
        for i in current_user.carts:
            if i.product.stock < i.quantity:
                continue

            item = OrderItem(order_id=order.id, product_id=i.product.id, quantity=i.quantity, price=i.product.price)
            db_sess.add(item)
            i.product.bought += i.quantity
            i.product.stock -= i.quantity
            db_sess.delete(i)

        db_sess.commit()
        return redirect("/orders")
    
    return render_template("checkout.html", title="К оплате", form=form)


@cart_bp.route('/orders')
def my_orders():
    if not current_user.is_authenticated:
        return abort(401)
    
    return render_template("orders.html", orders=sorted(current_user.orders, key=lambda x: x.created_date, reverse=True))