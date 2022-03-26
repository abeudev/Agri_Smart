from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Declaring application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc191a6dbce62114c5c47480'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///openagriculture.db'

# # Declaring Database
db = SQLAlchemy(app)
db.create_all()

from openagriculture import routes
