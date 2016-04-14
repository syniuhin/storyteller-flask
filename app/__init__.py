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

# Import a module / component using its blueprint handler variable (mod_auth)
from app.storyteller.controllers import storyteller

# Register blueprint(s)
app.register_blueprint(storyteller)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
