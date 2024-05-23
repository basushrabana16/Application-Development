# Author
Shrabana Basu
21F2001313

# Grocery Store Web Application
The Grocery-Store Application is a web-based application that allows multiple users to shop grocery items of different categories. The application has three parties - one admin, multiple managers and multiple users.The admin can remove managers or users and add/update/delete categories, while the managers can add/update/delete items. The users can browse items, search items, add items to cart.


## Tech Stack
- Flask: web framework for building the web application
- Flask-SQLAlchemy: ORM for connecting to the database and performing CRUD operations
- VueJS: Front end JavaScript library for building user interfaces and single-page applications.
- SQLite: database for storing user, shows, venues and booking data
- Bootstrap: Bootstrap version 5.3 is used in this project for the HTML styling and overall frontend designing. 
- Redis and Celery: Used for backend jobs


## Database Schema
- Signin - This table stores the details of the admins, managers and users like id, username, email, password.

- Category - This table stores the details of the all Category, like id and name.

- Item - This table stores the details of all Item, like id, name, description, manufacture_date, expiry_date, rate_per_unit, price, tags, image, item in stock etc. Each Item has it corresponding Category id.

- Cart- This table stores the details of the Item that are added to cart by any user. It shows the details of the items that are added like id, quantity.


The relationships between these tables are as follows:

- Category has one-to-many relationship with Item. That means each category can have multiple items.
- Item can be stored in Cart.


## Architecture and Features
The Model-View-Controller (MVC) paradigm is used to organise the entire project.The application provides user registration and login, CRUD of category/item by admin/manager, adding items to cart by users, searching multiple items by users, managers and admins.

The Grocery Store Application is a user-friendly and efficient web-based application that allows users to buy differeny items under different categories. The application provides an easy-to-use interface for browsing categories and items, and adding them to cart. The admin panel provides an efficient way to manage the application.


## Installation and Usage

The application can be rendered on a web server using the following steps:

- Clone the project
- Unzip the Project
- Open `21f2001313\Code` and open powershell/cmd at that path.
- Create a virtual environment with command `python -m venv {{Foldername}}` in cmd
- Activate the virtual environment with windows `{{Foldername}}\Scripts\activate`
- Activate the virtual environment with linux `source {{Foldername}}/bin/activate`


# Run celery
- Open `21f2001313\Code` and open another powershell/cmd at that path.
- Activate the virtual environment with `source {{Foldername}}/bin/activate`
- cd backend
- celery -A tasks worker -B

# Run redis
- Open `21f2001313\Code` and open another powershell/cmd at that path.
- Activate the virtual environment with `source {{Foldername}}/bin/activate`
- cd backend
- redis-server

# Run MailHog
- Open `21f2001313\Code` and open another powershell/cmd at that path.
- Activate the virtual environment with `source {{Foldername}}/bin/activate`
- cd backend
- ~/go/bin/MailHog

# Send email
- Open `21f2001313\Code` and open another powershell/cmd at that path.
- Activate the virtual environment with `source {{Foldername}}/bin/activate`
- cd backend/mail
- run `python send_email.py`

# Go to backend

- Open `21f2001313\Code` and open another powershell/cmd at that path.
- Activate the virtual environment with `source {{Foldername}}/bin/activate`
- cd backend
- Install the dependencies with `pip install -r requirements.txt`under created virtual environment.
- To run the flask app, on the shell, run `python app.py`
- Access the backend application at `http://localhost:5000`

# Go to frontend

- Open `21f2001313\Code` and open another powershell/cmd at that path.
- Activate the virtual environment with `source {{Foldername}}/bin/activate`
- cd backend
- Install npm packages `npm install`
- Install the Vue CLI `npm install -g @vue/cli`
- Run `npm run serve`
- Access the application at `http://localhost:8080/`

# Fing daily and monthly reminders
- Open localhost:8025