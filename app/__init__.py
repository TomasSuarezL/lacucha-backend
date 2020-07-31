import os
import config
from datetime import date

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api
from flask_cors import CORS

from .routes import register_routes

db = SQLAlchemy()
api = Api()


def create_app(_config=None):
    app = Flask(__name__)
    app.config.from_object(
        _config if _config != None else config.TestingConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api.init_app(app)
    register_routes(api, app)
    db.init_app(app)
    CORS(app)

    @app.route('/health')
    def health():
        result = db.session.execute('SELECT 1')
        print(result)
        return "Ok"

    return app
