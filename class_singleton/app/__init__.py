from flask import Flask

from .database import init_db


DATABASE_NAME = "app_data.sqlite3"


def create_app():

    app = Flask(__name__)

    app.config["DATABASE_PATH"] = DATABASE_NAME

    with app.app_context():
        init_db(app.config["DATABASE_PATH"])

    return app


app = create_app()


from . import routes