import pytest
from marshmallow.exceptions import ValidationError
from app.ejercicios.model import Ejercicio
from app.bloques.model import Bloque, EjercicioXBloque
from app.bloques.service import BloqueService


# Bloques SERVICE tests
def test_crear_bloque_x_ejercicio_valido(db):

    # Arrange
    ej_x_bloque = EjercicioXBloque(ejercicio=Ejercicio(
        "Traditional Push-ups"), repeticiones=10, carga=20.1)

    # Act
    exb = BloqueService.create_ejercicio_x_bloque(ej_x_bloque)

    # Assert
    assert exb.ejercicio.nombre == "Traditional Push-ups"
    assert exb.ejercicio.patron.nombre == "Tren Superior"
    assert exb.repeticiones == 10
    assert exb.carga == 20.1


def test_crear_bloque_x_ejercicio_ejercicio_invalido(db):
    # Arrange
    ej_x_bloque = EjercicioXBloque(ejercicio=Ejercicio(
        "Ejercicio No Existe"), repeticiones=12, carga=22.1)

    with pytest.raises(ValidationError) as excinfo:
        # ACT
        err, code = BloqueService.create_ejercicio_x_bloque(ej_x_bloque)


def test_crear_bloque_valido(db):
    # Arrange
    ej_x_bloque = EjercicioXBloque(ejercicio=Ejercicio(
        "Traditional Push-ups"), repeticiones=10, carga=20.1)

    bloque = Bloque(ejercicios=[ej_x_bloque], num_bloque=1, series=4)

    # Act
    bloque = BloqueService.create_bloque(bloque)

    # Assert
    assert bloque.series == 4
    assert bloque.num_bloque == 1
    assert len(bloque.ejercicios) == 1


# Bloques CONTROLLER tests
