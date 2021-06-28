from app.conftest import create_plantilla_db
from datetime import datetime
from app.plantillas.model import Plantilla


def test_controller_create_valid_plantilla(db, client, token):
    db
    # Arrange
    plantilla_data = {
        "nombre": "Prueba",
        "nivel": {"idNivel": 1},
        "objetivo": {"idObjetivo": 1},
        "organizacion": {"idOrganizacion": 1},
        "sesionesPorSemana": 2,
        "sesiones": [
            {
                "sesion": {
                    "idSesion": None,
                    "numSesion": 1,
                    "fechaEmpezado": str(datetime.utcnow()),
                    "bloques": [
                        {
                            "idBloque": None,
                            "series": 10,
                            "numBloque": 1,
                            "ejercicios": [
                                {
                                    "numEjercicio": 1,
                                    "ejercicio": {"idEjercicio": 1},
                                    "repeticiones": 10,
                                    "carga": 20.1,
                                }
                            ],
                        },
                        {
                            "idBloque": None,
                            "series": 10,
                            "numBloque": 2,
                            "ejercicios": [
                                {
                                    "numEjercicio": 1,
                                    "ejercicio": {"idEjercicio": 1},
                                    "repeticiones": 10,
                                    "carga": 20.1,
                                }
                            ],
                        },
                    ],
                },
            },
            {
                "sesion": {
                    "idSesion": None,
                    "numSesion": 2,
                    "fechaEmpezado": str(datetime.utcnow()),
                    "bloques": [
                        {
                            "idBloque": None,
                            "series": 10,
                            "numBloque": 1,
                            "ejercicios": [
                                {
                                    "numEjercicio": 1,
                                    "ejercicio": {"idEjercicio": 1},
                                    "repeticiones": 10,
                                    "carga": 20.1,
                                }
                            ],
                        },
                        {
                            "idBloque": None,
                            "series": 10,
                            "numBloque": 2,
                            "ejercicios": [
                                {
                                    "numEjercicio": 1,
                                    "ejercicio": {"idEjercicio": 1},
                                    "repeticiones": 10,
                                    "carga": 20.1,
                                }
                            ],
                        },
                    ],
                },
            },
        ],
    }
    # Act
    response = client.post(
        "/api/plantillas",
        json=plantilla_data,
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    plantilla = Plantilla.query.first()

    assert plantilla.nombre == "Prueba"
    assert plantilla.nivel.descripcion == "Principiante"
    assert plantilla.objetivo.descripcion == "Acondicionamiento General"
    assert plantilla.organizacion.descripcion == "Full Body"
    assert len(plantilla.sesiones) == 2


def test_controller_update_valid_plantilla(db, client, token):
    create_plantilla_db(db)
    # Arrange
    plantilla_data = {
        "nombre": "Prueba",
        "idPlantilla": 1,
        "nivel": {"idNivel": 2},
        "objetivo": {"idObjetivo": 2},
        "organizacion": {"idOrganizacion": 2},
        "sesionesPorSemana": 2,
        "sesiones": [
            {
                "idSesionesXPlantilla": 2,
                "sesion": {
                    "idSesion": None,
                    "numSesion": 2,
                    "fechaEmpezado": str(datetime.utcnow()),
                    "bloques": [
                        {
                            "idBloque": None,
                            "series": 10,
                            "numBloque": 1,
                            "ejercicios": [
                                {
                                    "numEjercicio": 1,
                                    "ejercicio": {"idEjercicio": 1},
                                    "repeticiones": 10,
                                    "carga": 20.1,
                                }
                            ],
                        },
                        {
                            "idBloque": None,
                            "series": 10,
                            "numBloque": 2,
                            "ejercicios": [
                                {
                                    "numEjercicio": 1,
                                    "ejercicio": {"idEjercicio": 1},
                                    "repeticiones": 10,
                                    "carga": 20.1,
                                }
                            ],
                        },
                    ],
                },
            },
        ],
    }
    # Act
    response = client.put(
        "/api/plantillas",
        json=plantilla_data,
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    plantilla = Plantilla.query.first()

    assert plantilla.nombre == "Prueba"
    assert plantilla.nivel.descripcion == "Intermedio"
    assert plantilla.objetivo.descripcion == "Hipertrofia"
    assert plantilla.organizacion.descripcion == "Tren Superior / Tren Inferior"
    assert len(plantilla.sesiones) == 1


def test_controller_delete_valid_plantilla(db, client, token):
    # Arrange
    create_plantilla_db(db)
    id_plantilla = 1

    # Act
    response = client.delete(
        f"/api/plantillas/{id_plantilla}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    plantilla = Plantilla.query.first()

    assert plantilla == None
