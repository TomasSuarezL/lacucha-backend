import os
import config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
import models

app.config.from_object(config.DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    "Add seed data to the database."
    ### EXERCISES ###

    traditionalPullUps = models.Exercise(
        name="Traditional Push-ups", zone="Upper Body")
    diamondPushUps = models.Exercise(
        name="Diamond Push-ups", zone="Upper Body")
    pullUps = models.Exercise(name="Pull-ups", zone="Upper Body")
    chinUps = models.Exercise(name="Chin-ups", zone="Upper Body")
    bulgarianSquats = models.Exercise(
        name="Bulgarian Squats", zone="Lower Body")
    skateSquats = models.Exercise(name="Skate Squats", zone="Lower Body")
    cossakSquats = models.Exercise(name="Cossak Squats", zone="Lower Body")
    hollowPress = models.Exercise(name="Hollow Press", zone="Middle Body")
    botesMov = models.Exercise(name="Botes Movimiento", zone="Middle Body")
    lAbs = models.Exercise(name="L-Abs", zone="Middle Body")
    db.session.add_all([traditionalPullUps, diamondPushUps, pullUps, chinUps,
                        bulgarianSquats, skateSquats, cossakSquats, hollowPress, botesMov, lAbs])

    db.session.commit()


if __name__ == '__main__':
    manager.run()
