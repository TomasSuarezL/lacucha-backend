import requests
import config
import os
from app.mesociclos.model import EstadoMesociclo, Mesociclo, Objetivo, Organizacion
from app.usuarios.model import Genero, Nivel, Usuario
from datetime import datetime, timedelta
from app.ejercicios.model import Ejercicio, PatronMovimiento
from app.bloques.model import Bloque, EjercicioXBloque
from app.sesiones.model import Sesion

import pytest

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
        create_reference_data(db)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()
        db.session.commit()


@pytest.fixture(scope="session")
def token():
    email = os.environ.get("TEST_USER_EMAIL")
    password = os.environ.get("TEST_USER_PASSWORD")
    response = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyD98jGZGIKFVLBQGgZi9MCdJeGho4zIlgI",
        data={"email": email, "password": password, "returnSecureToken": True,},
    )
    token = response.json().get("idToken")
    return token


def create_reference_data(db):
    # Patrones
    trenSuperior = PatronMovimiento(nombre="Tren Superior")
    trenInferior = PatronMovimiento(nombre="Tren Inferior")
    zonaMedia = PatronMovimiento(nombre="Zona Media")

    db.session.add_all([trenSuperior, trenInferior, zonaMedia])

    # Ejercicios
    traditionalPullUps = Ejercicio(nombre="Traditional Push-ups", patron=trenSuperior)
    diamondPushUps = Ejercicio(nombre="Diamond Push-ups", patron=trenSuperior)
    pullUps = Ejercicio(nombre="Pull-ups", patron=trenSuperior)
    chinUps = Ejercicio(nombre="Chin-ups", patron=trenSuperior)
    bulgarianSquats = Ejercicio(nombre="Bulgarian Squats", patron=trenInferior)
    skateSquats = Ejercicio(nombre="Skate Squats", patron=trenInferior)
    cossakSquats = Ejercicio(nombre="Cossak Squats", patron=trenInferior)
    hollowPress = Ejercicio(nombre="Hollow Press", patron=zonaMedia)
    botesMov = Ejercicio(nombre="Botes Movimiento", patron=zonaMedia)
    lAbs = Ejercicio(nombre="L-Abs", patron=zonaMedia)

    db.session.add_all(
        [
            traditionalPullUps,
            diamondPushUps,
            pullUps,
            chinUps,
            bulgarianSquats,
            skateSquats,
            cossakSquats,
            hollowPress,
            botesMov,
            lAbs,
        ]
    )

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


def create_sesion_db(db):
    ejSuperior = db.session.query(Ejercicio).first()
    ejInferior = db.session.query(Ejercicio).first()
    ejMedia = db.session.query(Ejercicio).first()

    exbSuperior = EjercicioXBloque(
        num_ejercicio=1, ejercicio=ejSuperior, repeticiones=10, carga=30
    )
    exbInferior = EjercicioXBloque(
        num_ejercicio=2, ejercicio=ejInferior, repeticiones=10, carga=50
    )
    exbMedia = EjercicioXBloque(
        num_ejercicio=3, ejercicio=ejMedia, repeticiones=15, carga=10
    )

    exbSuperior2 = EjercicioXBloque(
        num_ejercicio=1, ejercicio=ejSuperior, repeticiones=10, carga=30
    )
    exbInferior2 = EjercicioXBloque(
        num_ejercicio=2, ejercicio=ejInferior, repeticiones=10, carga=50
    )
    exbMedia2 = EjercicioXBloque(
        num_ejercicio=3, ejercicio=ejMedia, repeticiones=15, carga=10
    )

    nuevoBloque1 = Bloque(
        ejercicios=[exbSuperior, exbInferior, exbMedia], num_bloque=1, series=4
    )
    nuevoBloque2 = Bloque(
        ejercicios=[exbSuperior2, exbInferior2, exbMedia2], num_bloque=2, series=4
    )

    nuevaSesion = Sesion(
        bloques=[nuevoBloque1, nuevoBloque2], fecha_empezado=datetime.utcnow()
    )

    db.session.add(nuevaSesion)
    db.session.commit()


def create_usuario_db(db):
    genero = db.session.query(Genero).first()
    nivel = db.session.query(Nivel).first()

    usuario = Usuario(
        uuid="Oueo4BZj6iZPFyXFV04o8n7rVc83",
        username="usuarioprueba",
        email="usuario@prueba.com",
        nombre="Usuario",
        apellido="Prueba",
        fecha_nacimiento=datetime(1989, 8, 22),
        genero=genero,
        altura=1.77,
        peso=68,
        nivel=nivel,
        img_url="prueba.com/img",
        rol="admin",
    )

    db.session.add(usuario)
    db.session.commit()


def create_mesociclo_db(db):
    ejSuperior = db.session.query(Ejercicio).first()
    ejInferior = db.session.query(Ejercicio).first()
    ejMedia = db.session.query(Ejercicio).first()

    exbSuperior = EjercicioXBloque(
        num_ejercicio=1, ejercicio=ejSuperior, repeticiones=10, carga=30
    )
    exbInferior = EjercicioXBloque(
        num_ejercicio=2, ejercicio=ejInferior, repeticiones=10, carga=50
    )
    exbMedia = EjercicioXBloque(
        num_ejercicio=3, ejercicio=ejMedia, repeticiones=15, carga=10
    )

    exbSuperior2 = EjercicioXBloque(
        num_ejercicio=1, ejercicio=ejSuperior, repeticiones=10, carga=30
    )
    exbInferior2 = EjercicioXBloque(
        num_ejercicio=2, ejercicio=ejInferior, repeticiones=10, carga=50
    )
    exbMedia2 = EjercicioXBloque(
        num_ejercicio=3, ejercicio=ejMedia, repeticiones=15, carga=10
    )

    exbSuperior3 = EjercicioXBloque(
        num_ejercicio=1, ejercicio=ejSuperior, repeticiones=10, carga=30
    )
    exbInferior3 = EjercicioXBloque(
        num_ejercicio=2, ejercicio=ejInferior, repeticiones=10, carga=50
    )
    exbMedia3 = EjercicioXBloque(
        num_ejercicio=3, ejercicio=ejMedia, repeticiones=15, carga=10
    )

    exbSuperior4 = EjercicioXBloque(
        num_ejercicio=1, ejercicio=ejSuperior, repeticiones=10, carga=30
    )
    exbInferior4 = EjercicioXBloque(
        num_ejercicio=2, ejercicio=ejInferior, repeticiones=10, carga=50
    )
    exbMedia4 = EjercicioXBloque(
        num_ejercicio=3, ejercicio=ejMedia, repeticiones=15, carga=10
    )

    nuevoBloque1 = Bloque(
        ejercicios=[exbSuperior, exbInferior, exbMedia], num_bloque=1, series=4
    )
    nuevoBloque2 = Bloque(
        ejercicios=[exbSuperior2, exbInferior2, exbMedia2], num_bloque=2, series=4
    )

    nuevoBloque3 = Bloque(
        ejercicios=[exbSuperior3, exbInferior3, exbMedia3], num_bloque=1, series=4
    )
    nuevoBloque4 = Bloque(
        ejercicios=[exbSuperior4, exbInferior4, exbMedia4], num_bloque=2, series=4
    )

    nuevaSesion1 = Sesion(
        bloques=[nuevoBloque1, nuevoBloque2], fecha_empezado=datetime.utcnow()
    )
    nuevaSesion2 = Sesion(
        bloques=[nuevoBloque3, nuevoBloque4],
        fecha_empezado=datetime.utcnow() + timedelta(days=1),
    )

    usuario = db.session.query(Usuario).first()
    objetivo = db.session.query(Objetivo).first()
    organizacion = db.session.query(Organizacion).first()
    ej_superior = (
        db.session.query(Ejercicio).filter_by(nombre="Traditional Push-ups").first()
    )
    ej_inferior = (
        db.session.query(Ejercicio).filter_by(nombre="Bulgarian Squats").first()
    )

    mesociclo = Mesociclo(
        usuario=usuario,
        nivel=usuario.nivel,
        objetivo=objetivo,
        organizacion=organizacion,
        principal_tren_inferior=ej_inferior,
        principal_tren_superior=ej_superior,
        semanas_por_mesociclo=4,
        sesiones_por_semana=3,
        sesiones=[nuevaSesion1, nuevaSesion2],
    )

    db.session.add(mesociclo)
    db.session.commit()
