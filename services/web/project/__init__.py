from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application-Factory Method"""

    flask_app = Flask(__name__)
    flask_app.config.from_object("project.config.Config")

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    CORS(flask_app)
    flask_app.app_context().push()

    
    return flask_app
