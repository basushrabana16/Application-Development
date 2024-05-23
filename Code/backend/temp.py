from models import db
#from main import app
from app import app

with app.app_context():
    db.create_all()