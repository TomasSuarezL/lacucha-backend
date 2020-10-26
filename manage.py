from datetime import timedelta, datetime
import os
import config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import db
from app.mesociclos.model import EstadoMesociclo, Objetivo, Organizacion
from app.mesociclos.service import MesocicloService
from app.usuarios.model import Genero, Nivel, Usuario
from app.ejercicios.model import Ejercicio, PatronMovimiento

app = create_app(config.DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create():
    db.create_all()


@manager.command
def drop():
    db.drop_all()


@manager.command
def seed_reference_data():
    "Add seed data to the database."
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


@manager.command
def seed_initial_data():

    # Usuario
    genero = db.session.query(Genero).first()
    nivel = db.session.query(Nivel).first()

    user = Usuario(
        username="@tsuarezlissi",
        email="tomas.sl@hotmail.com",
        nombre="Tomas",
        apellido="Suarez Lissi",
        fecha_nacimiento=datetime(1989, 8, 22),
        genero=genero,
        altura=1.77,
        peso=68,
        nivel=nivel,
        img_url="https://flutter.github.io/assets-for-api-docs/assets/widgets/owl.jpg"
    )

    db.session.add(user)

    # Mesociclo
    sesion_data = {"empezado": str(datetime.utcnow()),
                   "finalizado": str(datetime.utcnow() + timedelta(hours=1)),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Pull-ups"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    mesociclo_data = {
        "usuario": "@tsuarezlissi",
        "nivel": "Intermedio",
        "objetivo": "Hipertrofia",
        "organizacion": "Full Body",
        "principal_tren_superior": "Traditional Push-ups",
        "principal_tren_inferior": "Bulgarian Squats",
        "semanas_por_mesociclo": 4,
        "sesiones_por_semana": 3,
        "sesiones": [sesion_data]
    }

    # Act
    mesociclo = MesocicloService.create_mesociclo(mesociclo_data)

    db.session.add(mesociclo)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
