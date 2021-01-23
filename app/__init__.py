import os
import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from flask_firebase_admin import FirebaseAdmin

from .routes import register_routes

db = SQLAlchemy()
api = Api()
firebase = FirebaseAdmin()


def create_app(_config=None):
    environ = os.environ.get("FLASK_ENV")
    if _config is None:
        _config = config.ProductionConfig if environ == 'production' else config.DevelopmentConfig
    app = Flask(__name__)
    app.config.from_object(_config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api.init_app(app)
    firebase.init_app(app)
    register_routes(api, app)
    db.init_app(app)
    CORS(app)

    @app.route('/health')
    def health():
        result = db.session.execute('SELECT 1')
        print(result)
        return "Ok"

    return app
