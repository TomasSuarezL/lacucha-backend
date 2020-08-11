from datetime import datetime
from app.ejercicios.model import Ejercicio, PatronMovimiento
from app.bloques.model import Bloque, EjercicioXBloque
from app.sesiones.model import Sesion
import os
import config

import pytest
from flask_sqlalchemy import SQLAlchemy

from app import create_app


@pytest.fixture
def app():
    return create_app(config.TestingConfig)


@pytest.fixture
def client(app): return app.test_client()


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


def create_sesion_db(db):
    superior = PatronMovimiento(nombre="Tren Superior")
    inferior = PatronMovimiento(nombre="Tren Inferior")
    media = PatronMovimiento(nombre="Zona Media")

    ejSuperior = Ejercicio(nombre="Ejercicio Tren Superior", patron=superior)
    ejInferior = Ejercicio(nombre="Ejercicio Tren Inferior", patron=inferior)
    ejMedia = Ejercicio(nombre="Ejercicio Zona Media", patron=media)

    db.session.add_all([ejSuperior, ejInferior, ejMedia])

    exbSuperior = EjercicioXBloque(
        ejercicio=ejSuperior, repeticiones=10, carga=30)
    exbInferior = EjercicioXBloque(
        ejercicio=ejInferior, repeticiones=10, carga=50)
    exbMedia = EjercicioXBloque(ejercicio=ejMedia, repeticiones=15, carga=10)

    nuevoBloque1 = Bloque(
        ejercicios=[exbSuperior, exbInferior, exbMedia], num_bloque=1, series=4)
    nuevoBloque2 = Bloque(
        ejercicios=[exbSuperior, exbInferior, exbMedia], num_bloque=2, series=4)

    nuevaSesion = Sesion(bloques=[nuevoBloque1, nuevoBloque2], fecha_empezado=datetime.utcnow(
    ), fecha_finalizado=datetime.utcnow())

    db.session.add(nuevaSesion)
    db.session.commit()
