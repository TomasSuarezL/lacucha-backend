import pytest
from marshmallow.exceptions import ValidationError
from app.conftest import create_ejercicio_db
from app.bloques.service import BloqueService


# Bloques SERVICE tests
def test_crear_bloque_x_ejercicio_valido(db):
    bloque_data = {"ejercicio": {"nombre": "Ejercicio"},
                   "repeticiones": 10, "carga": 20.1}
    create_ejercicio_db(db)

    exb = BloqueService.create_ejercicio_x_bloque(bloque_data)

    assert exb.ejercicio.nombre == "Ejercicio"
    assert exb.ejercicio.patron.nombre == "Zona Prueba"
    assert exb.repeticiones == 10
    assert exb.carga == 20.1


def test_crear_bloque_x_ejercicio_schema_invalido(db):
    bloque_data = {"ejercicio": {"nomsbre": "Ejercicio"},
                   "repeticiones": 22, "carga": 22.1}

    with pytest.raises(KeyError) as excinfo:

        err, code = BloqueService.create_ejercicio_x_bloque(bloque_data)


def test_crear_bloque_x_ejercicio_ejercicio_invalido(db):
    bloque_data = {"ejercicio": {"nombre": "Ejercicio No Existe"},
                   "repeticiones": 12, "carga": 22.1}
    create_ejercicio_db(db)

    with pytest.raises(ValidationError) as excinfo:

        err, code = BloqueService.create_ejercicio_x_bloque(bloque_data)


def test_crear_bloque_valido(db):
    bloque_data = {"series": 10,
                   "numBloque": 1,
                   "ejercicios": [{"ejercicio": {"nombre": "Ejercicio"}, "repeticiones": 10, "carga": 20.1}]}
    create_ejercicio_db(db)

    bloque = BloqueService.create_bloque(bloque_data)

    assert bloque.series == 10
    assert bloque.num_bloque == 1
    assert len(bloque.ejercicios) == 1


def test_crear_bloque_ejercicio_invalido(db):
    bloque_data = {"series": 10,
                   "numBloque": 1,
                   "ejercicios": [{"ejercicio": {"nombre": "Ejercicio"}, "repeticiones": 10, "carga": 20.1},
                                  {"ejercicio": {"nombre": "Ejercicio Invalido"}, "repeticiones": 12, "carga": 22.1}]}

    create_ejercicio_db(db)

    with pytest.raises(ValidationError) as excinfo:

        err, code = BloqueService.create_bloque(bloque_data)


# Bloques CONTROLLER tests
def test_post_bloque_valido(db, client):
    bloque_data = {"series": 10,
                   "numBloque": 1,
                   "ejercicios": [{"ejercicio": {"nombre": "Ejercicio"}, "repeticiones": 10, "carga": 20.1}]}
    create_ejercicio_db(db)

    response = client.post(
        '/api/bloques', json=bloque_data,  follow_redirects=True).get_json()

    print(response)

    assert response["series"] == 10
