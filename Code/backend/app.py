#basic imports
from flask import Flask, request, jsonify, session
from flask_restful import Api, Resource 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash
from flask_cors import CORS
from datetime import datetime
from flask_bcrypt import Bcrypt
import json
import time


#celery backeng jobs imports
from models import db, User, Category, Item, Cart
from worker import create_celery_app
import tasks
#from tasks import daily_reminder
from celery import Celery
from celery.result import AsyncResult
from flask_celeryext import FlaskCeleryExt


#caching imports
from flask_caching import Cache
from cach import cache


#export csv imports
from io import StringIO
import csv


#initialization
app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)


#configuration
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 30
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/2"
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)
cel_app = create_celery_app(app)
cache.init_app(app)

app.app_context().push()
security = Security()



@cel_app.task
def generate_csv():
    fields=["id","name","description","manufacture_date","expiry_date","price",
              "rate_per_unit","tags","iimg","item_in_stock","category_id","no. of items purchased"]
    
    csvfile = StringIO()
    csvwriter =csv.writer(csvfile)
    csvwriter.writerow(fields)

    items= Item.query.all()
    for item in items:
        item_purchase=Cart.query.filter_by(item_id=item.id).all()
        total=0
        for each in item_purchase:
            total+= each.quantity
    
        row = [
             item.id,
             item.name,
             item.description,
             item.manufacture_date,
             item.expiry_date,
             item.price,
             item.rate_per_unit,
             item.tags,
             item.iimg,
             item.item_in_stock,
             item.category_id,
             total
        ]
        csvwriter.writerow(row)

    csvfile.seek(0)
    return csvfile.read()
# ***********************************************************************************************************
# ***********************************************************************************************************


#CSV FILE
@app.route('/export-csv', methods=['GET'])
def export_csv():
    result= generate_csv.delay()
    return jsonify({"id":result.id})


@app.route('/download-csv', methods=['GET'])
def download_csv():
    result= AsyncResult(request.args.get("id"))
    if result.status!="SUCCESS":
        return jsonify({"status":result.status})
    return jsonify({"status":result.status,"data":result.result})
    

#REGISTER
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
     try:
        username = request.json.get('username')
        userType = request.json.get('userType')
        email = request.json.get('email')
        password = request.json.get('password')

        if not (username and userType and email and password):
            return jsonify({"message": "All fields are required"}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email is already registered"}), 400
        
        
        new_user = User(username=username, email=email, password=password, userType=userType)
        
        db.session.add(new_user)
        db.session.commit()

        
        return jsonify({"message": "User registered successfully"}), 201
    
     except Exception as e:
            print("An error occurred:", str(e))
            return jsonify({"message": str(e)}), 500
    else:
        return jsonify({"message": "Method not allowed"}), 405
    
def validate_user_role(user_type):
    allowed_roles = ['admin', 'manager', 'user']
    return user_type in allowed_roles


#LOGIN
@app.route('/login', methods=['POST'])
def login():
    try:
        user_type = request.json.get('userType')
        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter((User.email == email), (User.password == password)).first()

        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401

        if not validate_user_role(user_type):
            return jsonify({'message': 'Invalid role selected. Please try again.'}), 400
        

        session['user_id'] = user.id
        session['user_role'] = user_type

        # Debug log statements
        print("User logged in:", session['user_id'])
        print("User role:", session['user_role'])

        return jsonify({'message': 'Login successful'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500



#LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful','redirect': '/login'}), 200  
   

#GET EACH USER
@app.route('/all-user/<int:user_id>', methods=['GET'])
@cache.cached(10)
def get_user(user_id):
    print("get user with id function called")
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "userType" : user.userType,
        }
        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
# GET ALL USERS
@app.route('/all-user', methods=['GET'])
@cache.cached(10)
def get_all_users():
    print("all user function called")
    try:
        users = User.query.all()
        users_list = [{"id": user.id, "username": user.username, "email": user.email, "userType": user.userType} for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    

# DELETE USER
@app.route('/all-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 400





#ADD CATEGORY
@app.route('/add-category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        try:
            name = request.json.get('name')
            description = request.json.get('description')

            if not (name and description):
                return jsonify({"message": "Category name and description are required"}), 400

            if Category.query.filter_by(name=name).first():
                return jsonify({"message": "Category is already exists"}), 400

            new_category = Category(name=name, description=description)

            db.session.add(new_category)
            db.session.commit()

            return jsonify({"message": "Category added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"message": "Method not allowed"}), 405
    

#GET EACH CATEGORY
@app.route('/categories/<int:category_id>', methods=['GET'])
@cache.cached(10)
def get_category(category_id):
    print("categories with id function called")
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        category_data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
        }
        return jsonify(category_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


#UPDATE CATEGORY
@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        data = request.get_json()
        category.name = data.get('name')
        category.description = data.get('description')

        db.session.commit()

        return jsonify({"message": "Category updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# DELETE CATEGORY
@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted successfully"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 400



#GET ALL CATEGORY
@app.route('/categories', methods=['GET'])
@cache.cached(10)
def get_categories():
    print("categories function called")
    try:
        categories = Category.query.all()
        categories_list = [{"id": category.id, "name": category.name, "description": category.description} for category in categories]
        return jsonify(categories_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



#ADD ITEM
@app.route('/add-item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        try:
            name = request.json.get('name')
            description = request.json.get('description')
            manufacture_date_str = request.json.get('manufacture_date')
            expiry_date_str = request.json.get('expiry_date')
            price = request.json.get('price')
            rate_per_unit = request.json.get('rate_per_unit')
            tags = request.json.get('tags')
            iimg = request.json.get('iimg')
            item_in_stock = request.json.get('item_in_stock')
            category_id = request.json.get('category_id')

            manufacture_date = datetime.strptime(manufacture_date_str, '%Y-%m-%d').date()
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

            if not (name and description and manufacture_date and expiry_date and price and rate_per_unit and item_in_stock and category_id):
                return jsonify({"message": "Missing required fields"}), 400

            new_item = Item(name=name, description=description, manufacture_date=manufacture_date, expiry_date=expiry_date,
                            price=price, rate_per_unit=rate_per_unit, tags=tags, iimg=iimg, item_in_stock=item_in_stock,
                            category_id=category_id)

            db.session.add(new_item)
            db.session.commit()

            return jsonify({"message": "Item added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"message": "Method not allowed"}), 405
    


#GET EACH ITEM
@app.route('/items/<int:item_id>', methods=['GET'])
@cache.cached(10)
def get_item(item_id):
    print("items with id function called")
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        item_data = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "manufacture_date": item.manufacture_date,
            "expiry_date": item.expiry_date,
            "price": item.price,
            "rate_per_unit": str(item.rate_per_unit),
            "tags": item.tags,
            "iimg": item.iimg,
            "item_in_stock": item.item_in_stock,
            "category_id": item.category_id
        }
        return jsonify(item_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400



#UPDATE ITEM
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        data = request.get_json()
        item.name = data.get('name')
        item.description = data.get('description')
        item.manufacture_date = datetime.strptime(data.get('manufacture_date'), '%Y-%m-%d').date()
        item.expiry_date = datetime.strptime(data.get('expiry_date'), '%Y-%m-%d').date()
        item.price = data.get('price')
        item.rate_per_unit = data.get('rate_per_unit')
        item.tags = data.get('tags')
        item.iimg = data.get('iimg')
        item.item_in_stock = data.get('item_in_stock')
        item.category_id = data.get('category_id')

        db.session.commit()

        return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    


#DELETE ITEM (NEED TO BE MODIFIED)
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Item deleted successfully"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    


#GET ALL ITEM
@app.route('/items', methods=['GET'])
@cache.cached(10)
def get_items():
    print("items function called")
    try:
        items = Item.query.all()
        items_list = []
        for item in items:
            item_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "manufacture_date": item.manufacture_date.strftime('%Y-%m-%d'),
                "expiry_date": item.expiry_date.strftime('%Y-%m-%d'),
                "price": item.price,
                "rate_per_unit": item.rate_per_unit,
                "tags": item.tags,
                "iimg": item.iimg,
                "item_in_stock": item.item_in_stock,
                "category_id": item.category_id
            }
            items_list.append(item_data)
        return jsonify(items_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

#SEARCH
@app.route('/search', methods=['GET', 'POST'])
@cache.cached(10)
def search():
    print("search function called")
    if request.method == 'POST':
        search_query = request.json.get('search_query')

        if not search_query:
            return jsonify({"message": "Search query is required"}), 400

        results = []

        items_by_name = Item.query.filter(Item.name.ilike(f'%{search_query}%')).all()
        items_by_description = Item.query.filter(Item.description.ilike(f'%{search_query}%')).all()
        items_by_tag = Item.query.filter(Item.tags.ilike(f'%{search_query}%')).all()
        
        results.extend(items_by_name)
        results.extend(items_by_description)
        results.extend(items_by_tag)

        formatted_results = [
            {
                "name": item.name,
                "description": item.description,
                "tags": item.tags,
                "price": item.price,
            }
            for item in results
        ]

        return jsonify(formatted_results), 200

    return jsonify({"message": "Method not allowed"}), 405


#ADD-TO-CART
@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    try:
        item = Item.query.filter_by(id=item_id).first()
        if not item:
            return jsonify({"message": "Item not found"}), 404
        
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'message': 'You need to be logged in to add items to the cart'}), 401

        cart_item = Cart.query.filter_by(user_id=user_id, item_id=item_id).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * item.price
        else:
            cart_item = Cart(user_id=user_id, item_id=item_id, quantity=1, total_price=item.price)
            db.session.add(cart_item)

        db.session.commit()

        return jsonify({'message': 'Item added to cart successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    

#USER-CART-ITEMS
@app.route('/user-cart-items', methods=['GET'])
@cache.cached(10)
def get_user_cart_items():
    print("user cart items function called")
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'message': 'You need to be logged in to view your cart'}), 401

        cart_items = Cart.query.filter_by(user_id=user_id).all()
        cart_items_data = [{
            'item_id': cart_item.item_id,
            'item_name': cart_item.item.name,
            'quantity': cart_item.quantity,
            'total_price': cart_item.total_price
        } for cart_item in cart_items]

        return jsonify(cart_items_data), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

#REMOVE-FROM-CART
@app.route('/remove-from-cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'message': 'You need to be logged in to remove items from your cart'}), 401

        cart_item = Cart.query.filter_by(user_id=user_id, item_id=item_id).first()
        if not cart_item:
            return jsonify({'message': 'Item not found in your cart'}), 404

        db.session.delete(cart_item)
        db.session.commit()

        return jsonify({'message': 'Item removed from cart successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# ***********************************************************************************************************
# ***********************************************************************************************************
if __name__ == '__main__':
    app.run(debug=True, port=5000)

