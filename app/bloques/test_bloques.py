import pytest
from marshmallow.exceptions import ValidationError
from app.conftest import create_usuario_db, create_mesociclo_db
from app.ejercicios.model import Ejercicio
from app.bloques.model import Bloque, EjercicioXBloque
from app.bloques.service import BloqueService


# Bloques SERVICE tests
def test_crear_bloque_x_ejercicio_valido(db):

    # Arrange
    ej_x_bloque = EjercicioXBloque(
        ejercicio=Ejercicio("Traditional Push-ups"), repeticiones=10, carga=20.1
    )

    # Act
    exb = BloqueService.create_ejercicio_x_bloque(ej_x_bloque)

    # Assert
    assert exb.ejercicio.nombre == "Traditional Push-ups"
    assert exb.ejercicio.patron.nombre == "Tren Superior"
    assert exb.repeticiones == 10
    assert exb.carga == 20.1


def test_crear_bloque_x_ejercicio_ejercicio_invalido(db):
    # Arrange
    ej_x_bloque = EjercicioXBloque(
        ejercicio=Ejercicio("Ejercicio No Existe"), repeticiones=12, carga=22.1
    )

    with pytest.raises(ValidationError) as excinfo:
        # ACT
        err, code = BloqueService.create_ejercicio_x_bloque(ej_x_bloque)


def test_crear_bloque_valido(db):
    # Arrange
    ej_x_bloque = EjercicioXBloque(
        ejercicio=Ejercicio("Traditional Push-ups"), repeticiones=10, carga=20.1
    )

    bloque = Bloque(ejercicios=[ej_x_bloque], num_bloque=1, series=4)

    # Act
    bloque = BloqueService.create_bloque(bloque)

    # Assert
    assert bloque.series == 4
    assert bloque.num_bloque == 1
    assert len(bloque.ejercicios) == 1


# Bloques CONTROLLER tests
def test_crear_bloque_valido(db, token, client):

    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    bloque_update_body = {
        "idBloque": 1,
        "numBloque": 3,  # el num_bloque pasaria de 1 a 3
        "series": 5,  # las series deberian pasar de 4 a 5
        "ejercicios": [
            {
                "idEjerciciosxbloque": 1,  # Cambio el primer ejercicio
                "repeticiones": 20,  # Paso de 10 reps a 20
                "carga": 150,  # paso de 30kg a 150kg
                "ejercicio": {
                    "idEjercicio": 5,  # Paso de Traditional Push-ups a Bulgarian Squats
                },
            }
        ],
    }

    # Act

    bloque_response = client.put(
        "/api/bloques",
        json=bloque_update_body,
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    bloque = Bloque.query.filter_by(id_bloque=1).first()

    assert bloque_response != None
    assert bloque.id_bloque == 1
    assert bloque.num_bloque == 3
    assert bloque.series == 5
    assert bloque.ejercicios[0].repeticiones == 20
