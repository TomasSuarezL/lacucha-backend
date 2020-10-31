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
    create_usuario_db(db)
    create_sesion_db(db)

    # Act
    sesion_hoy = SesionService.get_today_sesion()

    # Assert
    assert sesion_hoy is not None
    assert len(sesion_hoy.bloques) == 2


# Sesion CONTROLLER tests
def test_controller_create_sesion(db, client):
    sesion_body = {
        "fechaEmpezado": str(datetime.utcnow()),
        "fechaFinalizado": str(datetime.utcnow() + timedelta(hours=1)),
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

    rv = client.post('/api/sesiones', json=sesion_body,
                     follow_redirects=True).get_json()

    assert len(rv['bloques']) == 1
    assert len(rv['bloques'][0]["ejercicios"]) == 1
    assert rv['bloques'][0]["ejercicios"][0]['ejercicio']['patron'] == "Tren Superior"
