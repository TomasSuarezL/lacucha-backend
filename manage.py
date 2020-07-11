import os
import config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import db
from app.ejercicios.model import Ejercicio, PatronMovimiento

app = create_app(config.TestingConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    "Add seed data to the database."
    ### EXERCISES ###
    trenSuperior = PatronMovimiento(nombre="Tren Superior")
    trenInferior = PatronMovimiento(nombre="Tren Inferior")
    zonaMedia = PatronMovimiento(nombre="Zona Media")

    db.session.add_all([trenSuperior, trenInferior, zonaMedia])

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

    db.session.commit()


if __name__ == '__main__':
    manager.run()
