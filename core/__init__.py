
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

from config import Configuration


""" 
    This file contains the initialization of the application.
    * Construct and configure flask application.
    * Create database connection and configure the database.
    * Register modules as flask blueprints.
    * Import core application views. 
"""

# Create the flask application instance
app = Flask(__name__)

# Register application configuration settings
app.config.from_object(Configuration)

# Create the database connection and register the application
db = SQLAlchemy(app)

# Create the database connection, register the application, and apply migration naming conventions.
naming_convention = {
    'ix': 'ix_$(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

# Apply the naming_convention to the database
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

# Allow database migrations
migrate = Migrate(app, db, render_as_batch=True)


# register application blueprints
from .user_auth import user_auth as user_auth_blueprint
app.register_blueprint(user_auth_blueprint)


# import the core application views
from core import views


