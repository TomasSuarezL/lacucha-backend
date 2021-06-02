import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from flask_firebase_admin import FirebaseAdmin
from flask_migrate import Migrate

from .routes import register_routes

db = SQLAlchemy()
api = Api()
firebase = FirebaseAdmin()
migrate = Migrate()


def create_app(_config=None):
    environ = os.environ.get("FLASK_ENV")
    if _config is None:
        _config = (
            config.ProductionConfig
            if environ == "production"
            else config.DevelopmentConfig
        )
    app = Flask(__name__)
    app.config.from_object(_config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or app.config["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    api.init_app(app)
    firebase.init_app(app)
    register_routes(api, app)
    db.init_app(app)
    CORS(app)
    migrate.init_app(app, db)

    @app.route("/health")
    def health():
        result = db.session.execute("SELECT 1")
        print(result)
        return "Ok"

    return app
