from app.mesociclos.model import EstadoMesociclo, Objetivo, Organizacion
from app.usuarios.model import Genero, Nivel, Usuario
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
        create_reference_data(db)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()
        db.session.commit()


def create_reference_data(db):
    # Patrones
    trenSuperior = PatronMovimiento(nombre="Tren Superior")
    trenInferior = PatronMovimiento(nombre="Tren Inferior")
    zonaMedia = PatronMovimiento(nombre="Zona Media")

    db.session.add_all([trenSuperior, trenInferior, zonaMedia])

    # Ejercicios
    traditionalPullUps = Ejercicio(
        nombre="Traditional Push-ups", patron=trenSuperior)
    diamondPushUps = Ejercicio(
        nombre="Diamond Push-ups", patron=trenSuperior)
    pullUps = Ejercicio(nombre="Pull-ups", patron=trenSuperior)
    chinUps = Ejercicio(nombre="Chin-ups", patron=trenSuperior)
    bulgarianSquats = Ejercicio(
        nombre="Bulgarian Squats", patron=trenInferior)
    skateSquats = Ejercicio(nombre="Skate Squats", patron=trenInferior)
    cossakSquats = Ejercicio(nombre="Cossak Squats", patron=trenInferior)
    hollowPress = Ejercicio(nombre="Hollow Press", patron=zonaMedia)
    botesMov = Ejercicio(nombre="Botes Movimiento", patron=zonaMedia)
    lAbs = Ejercicio(nombre="L-Abs", patron=zonaMedia)

    db.session.add_all([traditionalPullUps, diamondPushUps, pullUps, chinUps,
                        bulgarianSquats, skateSquats, cossakSquats, hollowPress, botesMov, lAbs])

    # Niveles
    principiante = Nivel("Principiante")
    intermedio = Nivel("Intermedio")
    avanzado = Nivel("Avanzado")
    db.session.add_all([principiante, intermedio, avanzado])

    # Generos
    masculino = Genero("Masculino")
    femenino = Genero("Femenino")
    otro = Genero("Otro")
    db.session.add_all([masculino, femenino, otro])

    # Estados Mesociclo
    activo = EstadoMesociclo("Activo")
    terminado = EstadoMesociclo("Terminado")
    cancelado = EstadoMesociclo("Cancelado")
    db.session.add_all([activo, terminado, cancelado])

    # Organizaciones
    fullBody = Organizacion("Full Body")
    tsti = Organizacion("Tren Superior / Tren Inferior")
    combinado = Organizacion("Combinado")
    db.session.add_all([fullBody, tsti, combinado])

    # Objetivos
    acondicionamientoGeneral = Objetivo("Acondicionamiento General")
    hipertrofia = Objetivo("Hipertrofia")
    fuerza = Objetivo("Fuerza")
    db.session.add_all([acondicionamientoGeneral, hipertrofia, fuerza])

    db.session.commit()


def create_ejercicio_db(db):
    patron = PatronMovimiento(nombre="Zona Prueba")

    nuevoEjercicio = Ejercicio(nombre="Ejercicio", patron=patron)

    db.session.add(nuevoEjercicio)
    db.session.commit()


def create_sesion_db(db):
    ejSuperior = Ejercicio.query.first()
    ejInferior = Ejercicio.query.first()
    ejMedia = Ejercicio.query.first()

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


def create_usuario_db(db):
    genero = db.session.query(Genero).first()
    nivel = db.session.query(Nivel).first()

    user = Usuario(
        username="usuarioprueba",
        email="usuario@prueba.com",
        nombre="Usuario",
        apellido="Prueba",
        fecha_nacimiento=datetime(1989, 8, 22),
        genero=genero,
        altura=1.77,
        peso=68,
        nivel=nivel,
    )

    db.session.add(user)
    db.session.commit()
