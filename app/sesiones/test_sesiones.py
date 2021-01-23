from app.ejercicios.model import Ejercicio
from app.sesiones.model import Sesion
from app.bloques.model import Bloque, EjercicioXBloque
from app.conftest import create_sesion_db, create_usuario_db
from app.sesiones.service import SesionService
from datetime import datetime, timedelta


# Sesion SERVICE Tests
def test_create_sesion(db):
    # Arrange
    ej_x_bloque = EjercicioXBloque(ejercicio=Ejercicio(
        "Traditional Push-ups"), repeticiones=10, carga=20.1)

    bloque = Bloque(ejercicios=[ej_x_bloque], num_bloque=1, series=4)

    sesion = Sesion(fecha_empezado=str(datetime.utcnow()), fecha_finalizado=str(
        datetime.utcnow() + timedelta(hours=1)), bloques=[bloque])

    # Act
    sesion = SesionService.create_sesion(sesion)

    # Assert
    assert len(sesion.bloques) == 1


def test_get_today_sesion(db):
    # Arrange
    create_sesion_db(db)

    # Act
    sesion_hoy = SesionService.get_today_sesion()

    # Assert
    assert sesion_hoy is not None
    assert len(sesion_hoy.bloques) == 2


# Sesion CONTROLLER tests
def test_controller_create_sesion(db, client):
    # Arrange
    sesion_body = {
        "fechaEmpezado": str(datetime.utcnow()),
        "bloques": [
            {"numBloque": 1,
             "series": 4,
             "ejercicios": [
                 {"ejercicio": {"nombre": "Traditional Push-ups"},
                  "repeticiones": 10,
                  "carga": 20.1}
             ]
             }
        ]
    }

    # Act
    rv = client.post('/api/sesiones', json=sesion_body,
                     follow_redirects=True).get_json()

    # Assert
    sesion = Sesion.query.first()

    assert len(sesion.bloques) == 1
    assert len(sesion.bloques[0].ejercicios) == 1
    assert sesion.bloques[0].ejercicios[0].ejercicio.patron.nombre == "Tren Superior"


def test_controller_update_sesion(db, client):
    # Arrange
    create_sesion_db(db)
    id_sesion = 1

    sesion_body = {
        "idSesion": 1,
        "fechaFinalizado": str(datetime.utcnow() + timedelta(hours=1)),
        "fechaEmpezado": str(datetime(2020, 11, 1)),
        "bloques": [
            {"idBloque": 1,
             "numBloque": 1,
             "series": 5,
             "ejercicios": [
                 {"idEjerciciosxbloque": 1,
                  "ejercicio": {"idEjercicio": 2},
                  "repeticiones": 16,
                  "carga": 20.1},
                 {"idEjerciciosxbloque": 2},
                 {"idEjerciciosxbloque": 3}
             ]
             },
            {"idBloque": 2}
        ]
    }

    # Act
    rv = client.put(
        f'/api/sesiones/{str(id_sesion)}', json=sesion_body, follow_redirects=True).get_json()

    sesion = Sesion.query.first()

    # Assert
    assert sesion.fecha_finalizado != None
    assert sesion.fecha_empezado.date() == datetime(2020, 11, 1).date()
    assert len(sesion.bloques) == 2
    assert len(sesion.bloques[0].ejercicios) == 3
    bloques = sorted(sesion.bloques, key=lambda k: k.id_bloque)
    bloque1_ejercicios = sorted(
        bloques[0].ejercicios, key=lambda k: k.id_ejerciciosxbloque)
    assert bloque1_ejercicios[0].repeticiones == 16
    assert bloque1_ejercicios[0].carga == 20.1
    assert bloque1_ejercicios[0].ejercicio.nombre == "Diamond Push-ups"
    assert bloque1_ejercicios[0].ejercicio.patron.nombre == "Tren Superior"
    assert bloque1_ejercicios[1].repeticiones == 10
    assert bloque1_ejercicios[1].carga == 50
    assert bloque1_ejercicios[1].ejercicio.nombre == "Traditional Push-ups"
    assert bloque1_ejercicios[1].ejercicio.patron.nombre == "Tren Superior"


def test_controller_get_today_sesion(db, client):
    # Arrange
    create_sesion_db(db)

    # Act
    rv = client.get(
        f'/api/sesiones/todaySesion', follow_redirects=True).get_json()

    # Assert
    assert len(rv['bloques']) == 2
    assert len(rv['bloques'][0]["ejercicios"]) == 3
    assert rv['bloques'][0]["ejercicios"][1]["repeticiones"] == 10
    assert rv['bloques'][0]["ejercicios"][1]["carga"] == 30
    assert rv['bloques'][0]["ejercicios"][1]["ejercicio"]["nombre"] == "Traditional Push-ups"
    assert rv['bloques'][0]["ejercicios"][1]["ejercicio"]["patron"]["nombre"] == "Tren Superior"
