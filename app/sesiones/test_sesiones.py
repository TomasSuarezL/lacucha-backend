from app.mesociclos.model import Mesociclo
from app.ejercicios.model import Ejercicio
from app.sesiones.model import Sesion
from app.bloques.model import Bloque, EjercicioXBloque
from app.conftest import create_mesociclo_db, create_sesion_db, create_usuario_db
from app.sesiones.service import SesionService
from datetime import datetime, timedelta


# Sesion SERVICE Tests
def test_create_sesion(db):
    # Arrange
    ej_x_bloque = EjercicioXBloque(
        ejercicio=Ejercicio("Traditional Push-ups"), repeticiones=10, carga=20.1
    )

    bloque = Bloque(ejercicios=[ej_x_bloque], num_bloque=1, series=4)

    sesion = Sesion(
        fecha_empezado=str(datetime.utcnow()),
        fecha_finalizado=str(datetime.utcnow() + timedelta(hours=1)),
        bloques=[bloque],
    )

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
def test_controller_create_sesion(db, client, token):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)
    sesion_body = {
        "idMesociclo": 1,
        "fechaEmpezado": str(datetime.utcnow()),
        "bloques": [
            {
                "numBloque": 1,
                "series": 4,
                "ejercicios": [
                    {
                        "ejercicio": {"idEjercicio": 1},
                        "numEjercicio": 1,
                        "repeticiones": 10,
                        "carga": 20.1,
                    }
                ],
            }
        ],
    }

    # Act
    rv = client.post(
        "/api/sesiones",
        json=sesion_body,
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    mesociclo = Mesociclo.query.first()

    assert len(mesociclo.sesiones) == 3
    sesion = sorted(mesociclo.sesiones, key=lambda s: s.id_sesion)[2]
    assert len(sesion.bloques[0].ejercicios) == 1
    assert sesion.bloques[0].ejercicios[0].ejercicio.patron.nombre == "Tren Superior"


def test_controller_update_sesion(db, client, token):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)
    id_sesion = 1

    sesion_body = {
        "idMesociclo": 1,
        "idSesion": 1,
        "fechaFinalizado": str(datetime.utcnow() + timedelta(hours=1)),
        "fechaEmpezado": str(datetime(2020, 11, 1)),
        "bloques": [
            {
                "idBloque": 1,
                "numBloque": 1,
                "series": 5,
                "ejercicios": [
                    {
                        "idEjerciciosxbloque": 1,
                        "numEjercicio": 5,
                        "ejercicio": {"idEjercicio": 2},
                        "repeticiones": 16,
                        "carga": 20.1,
                    },
                    {"idEjerciciosxbloque": 2},
                    {"idEjerciciosxbloque": 3},
                    # Agrego un ej
                    {
                        "ejercicio": {"idEjercicio": 2},
                        "numEjercicio": 4,
                        "repeticiones": 20,
                        "carga": 22,
                    },
                ],
            },
            ## {"idBloque": 2},  No mando el bloque2 ("eliminado")
            ## Agrego un nuevo bloque
            {
                "numBloque": 2,
                "series": 6,
                "ejercicios": [
                    {
                        "ejercicio": {"idEjercicio": 2},
                        "numEjercicio": 1,
                        "repeticiones": 20,
                        "carga": 22,
                    },
                    {
                        "ejercicio": {"idEjercicio": 1},
                        "numEjercicio": 2,
                        "repeticiones": 21,
                        "carga": 23,
                    },
                    {
                        "ejercicio": {"idEjercicio": 3},
                        "numEjercicio": 3,
                        "repeticiones": 22,
                        "carga": 24,
                    },
                ],
            },
        ],
    }

    # Act
    rv = client.put(
        f"/api/sesiones/{str(id_sesion)}",
        json=sesion_body,
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    sesion = Sesion.query.get(1)

    # Assert
    assert sesion.fecha_finalizado != None
    assert sesion.fecha_empezado.date() == datetime(2020, 11, 1).date()
    assert len(sesion.bloques) == 2
    assert len(sesion.bloques[0].ejercicios) == 4
    bloques = sorted(sesion.bloques, key=lambda k: k.id_bloque)
    bloque1_ejercicios = sorted(
        bloques[0].ejercicios, key=lambda k: k.id_ejerciciosxbloque
    )
    bloque2_ejercicios = sorted(
        bloques[1].ejercicios, key=lambda k: k.id_ejerciciosxbloque
    )
    assert bloque1_ejercicios[0].repeticiones == 16
    assert bloque1_ejercicios[0].carga == 20.1
    assert bloque1_ejercicios[0].num_ejercicio == 5
    assert bloque1_ejercicios[0].ejercicio.nombre == "Diamond Push-ups"
    assert bloque1_ejercicios[0].ejercicio.patron.nombre == "Tren Superior"
    assert bloque2_ejercicios[0].carga == 22
    assert bloque2_ejercicios[0].ejercicio.nombre == "Diamond Push-ups"
    assert bloque2_ejercicios[0].ejercicio.patron.nombre == "Tren Superior"
    assert bloque2_ejercicios[0].repeticiones == 20


def test_controller_delete_sesion(db, client, token):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)
    id_sesion = 1

    # Act
    rv = client.delete(
        f"/api/sesiones/{id_sesion}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    sesion = Sesion.query.get(id_sesion)

    assert sesion == None


def test_controller_get_today_sesion(db, client):
    # Arrange
    create_sesion_db(db)

    # Act
    rv = client.get(f"/api/sesiones/todaySesion", follow_redirects=True).get_json()

    # Assert
    assert len(rv["bloques"]) == 2
    assert len(rv["bloques"][0]["ejercicios"]) == 3
    assert rv["bloques"][0]["ejercicios"][1]["repeticiones"] == 10
    assert rv["bloques"][0]["ejercicios"][1]["carga"] == 30
    assert (
        rv["bloques"][0]["ejercicios"][1]["ejercicio"]["nombre"]
        == "Traditional Push-ups"
    )
    assert (
        rv["bloques"][0]["ejercicios"][1]["ejercicio"]["patron"]["nombre"]
        == "Tren Superior"
    )
