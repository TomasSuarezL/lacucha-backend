from app.ejercicios.model import Ejercicio, PatronMovimiento
import os
import config

import pytest
from flask_sqlalchemy import SQLAlchemy

from app import create_app


@pytest.fixture
def app():
    return create_app(config.TestingConfig)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from app import db
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.commit()
        db.drop_all()


def create_ejercicio_db(db):
    patron = PatronMovimiento(nombre="Zona Prueba")

    nuevoEjercicio = Ejercicio(nombre="Ejercicio", patron=patron)

    db.session.add(nuevoEjercicio)
    db.session.commit()
