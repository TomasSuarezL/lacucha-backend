import pytest
from manage import seed
from app.conftest import create_ejercicio_db
from app.ejercicios.model import Ejercicio, PatronMovimiento
from app.ejercicios.service import EjercicioService


@pytest.mark.skip(reason="Trivial test of db seed")
def test_ejercicios_seedeados(db):
    seed()

    row = Ejercicio.query.filter_by(
        nombre="Traditional Push-ups").first()

    assert row.nombre == 'Traditional Push-ups'
    assert row.patron.nombre == 'Tren Superior'


def test_crear_ejercicio_model(db):
    create_ejercicio_db(db)

    ejercicio = Ejercicio.query.filter_by(
        nombre="Ejercicio").first()

    assert ejercicio.nombre == "Ejercicio"


# SERVICE TESTS
def test_service_get_ejercicio_por_nombre(db):
    create_ejercicio_db(db)

    ejercicio = EjercicioService.get_por_nombre("Ejercicio")

    assert isinstance(ejercicio, Ejercicio)
    assert ejercicio.nombre == "Ejercicio"
    assert ejercicio.patron.nombre == "Zona Prueba"


@pytest.mark.parametrize("test_input,expected", [("", None), ("Push-ups", None)])
def test_service_get_ejercicio_por_nombre_invalido(db, test_input, expected):
    ejercicio = EjercicioService.get_por_nombre(test_input)

    assert ejercicio is None


def test_service_crear_ejercicio_nuevo(db):
    patron = PatronMovimiento(nombre="Tren Superior")
    db.session.add(patron)
    db.session.commit()

    ejercicio = EjercicioService.create_ejercicio(
        nombre="Nuevo Ejercicio", patron="Tren Superior")

    assert isinstance(ejercicio, Ejercicio)
    assert ejercicio.nombre == "Nuevo Ejercicio"
    assert ejercicio.patron.nombre == "Tren Superior"


@pytest.mark.parametrize("nombre,patron", [("", "Tren Superior"), (None, "Tren Superior"), ("Nuevo Ejercicio", "Tren Superior"), ("Nuevo Ejercicio", None)])
def test_service_no_crea_ejercicio_con_patron_inexistente(db, nombre, patron):

    ejercicio = EjercicioService.create_ejercicio(
        nombre=nombre, patron=patron)

    assert type(ejercicio) is str


# CONTROLLER TESTS
def test_controller_list_ejercicios(db, client):
    create_ejercicio_db(db)

    rv = client.get('/api/ejercicios?patron=Zona Prueba',
                    follow_redirects=True).get_json()
    print(rv)

    assert len(rv) == 1
