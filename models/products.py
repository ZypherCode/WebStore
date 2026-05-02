import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Products(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    tags = sqlalchemy.Column(sqlalchemy.String)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    stock = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    good_marks = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    bad_marks = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    showed = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    clicked = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    bought = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User', back_populates='products')
    reviews = orm.relationship('Review', back_populates='product')