# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# We import all of our controllers first to help Blueprints initialize properly.
from app.storyteller.controllers import image_controller, user_controller
from app.storyteller.controllers import storyteller

# Register blueprint(s)
app.register_blueprint(storyteller)

# Build the database:
# This will create the database file using SQLAlchemy
from app.storyteller.models import Story, User, UploadedFile

db.create_all()
