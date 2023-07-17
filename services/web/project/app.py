from flask import jsonify

# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from flask_migrate import Migrate

from project import create_app, db
from project.controllers.user import user_bp
from project.controllers.projects import project_bp
from project.controllers.task import task_bp

app = create_app()

# db = SQLAlchemy(app)
# migrate = Migrate(app)
# CORS(app)
# print("db :", db)

@app.route("/")
def index():
    return jsonify(message="Welcome to docker-flask"), 200

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(project_bp, url_prefix="/projects")
app.register_blueprint(task_bp, url_prefix="/task")