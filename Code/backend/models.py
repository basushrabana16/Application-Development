from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

class Sum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Integer)
    b = db.Column(db.Integer)

    def __init__(self, a, b):
        self.a = a
        self.b = b


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    userType = db.Column(db.String(50), nullable=False, default='user')

    def __init__(self, username, email, password, userType='user'):
        self.username = username
        self.email = email
        self.password = password
        self.userType = userType

    def __repr__(self):
        return f'<User {self.username}>'



    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Category {self.name}>'
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.Date, nullable=True)
    expiry_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rate_per_unit = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    tags = db.Column(db.String(100))
    iimg=db.Column(db.String(2000))
    item_in_stock= db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    category = db.relationship('Category', backref=db.backref('category_relation', lazy=True))

    def __init__(self, name, description, manufacture_date, expiry_date, price, rate_per_unit, tags, iimg, item_in_stock, category_id):
        self.name = name
        self.description = description
        self.manufacture_date = manufacture_date
        self.expiry_date = expiry_date
        self.price = price
        self.rate_per_unit = rate_per_unit
        self.tags = tags
        self.iimg = iimg
        self.item_in_stock = item_in_stock
        self.category_id = category_id

    def __repr__(self):
        return f'<Item {self.name}>'
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship('Item', backref=db.backref('cart_items', lazy=True))

    def __init__(self, user_id, item_id, quantity, total_price):
        self.user_id = user_id
        self.item_id = item_id
        self.quantity = quantity
        self.total_price = total_price

    def __repr__(self):
        return f'<Cart {self.user_id} - {self.item_id}>'