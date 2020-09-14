from app.mesociclos.model import Mesociclo
import pytest
from marshmallow.exceptions import ValidationError
from app.mesociclos.service import MesocicloService
from app.conftest import create_ejercicio_db, create_usuario_db
from datetime import datetime, timedelta


# Service
def test_crear_mesociclo_valido(db):
    # Arrange
    create_usuario_db(db)
    sesion_data = {"empezado": str(datetime.utcnow()),
                   "finalizado": str(datetime.utcnow() + timedelta(hours=1)),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Pull-ups"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    mesociclo_data = {
        "usuario": "usuarioprueba",
        "nivel": "Intermedio",
        "objetivo": "Hipertrofia",
        "organizacion": "Full Body",
        "principal_tren_superior": "Traditional Push-ups",
        "principal_tren_inferior": "Bulgarian Squats",
        "semanas_por_mesociclo": 4,
        "sesiones_por_semana": 3,
        "sesiones": [sesion_data]
    }

    # Act
    mesociclo = MesocicloService.create_mesociclo(mesociclo_data)

    # Assert
    assert mesociclo.usuario.username == "usuarioprueba"
    assert mesociclo.objetivo.descripcion == "Hipertrofia"
    assert mesociclo.organizacion.descripcion == "Full Body"
    assert mesociclo.principal_tren_superior.nombre == "Traditional Push-ups"
    assert mesociclo.semanas_por_mesociclo == 4
    assert len(mesociclo.sesiones) == 1


def test_crear_mesociclo_invalido(db):
    # Arrange
    create_usuario_db(db)
    sesion_data = {"empezado": str(datetime.utcnow()),
                   "finalizado": str(datetime.utcnow() + timedelta(hours=1)),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Pull-ups"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    mesociclo_data = {
        "usuario": "usuarioprueba",  # Usuario inválido
        "nivel": "Intermedio",  # Nivel inválido
        "objetivo": "Hipertrofia",  # Objetivo inválido
        "organizacion": "Full Body",  # Organizacion inválida
        "principal_tren_superior": "Traditional Push-ups",  # Ejercicio TS inválido
        "principal_tren_inferior": "Bulgarian Squats",  # Ejercicio TI inválido
        "semanas_por_mesociclo": 4,
        "sesiones_por_semana": 3,
        "sesiones": [sesion_data]  # Sesiones vacias
    }

    # Act
    with pytest.raises(ValidationError) as excinfo:
        mesociclo = MesocicloService.create_mesociclo(mesociclo_data)


# Controller
def test_controller_crear_mesociclo_valido(db, client):
    # Arrange
    create_usuario_db(db)
    sesion_data = {"empezado": str(datetime.utcnow()),
                   "finalizado": str(datetime.utcnow() + timedelta(hours=1)),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Pull-ups"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    mesociclo_data = {
        "usuario": "usuarioprueba",
        "nivel": "Intermedio",
        "objetivo": "Hipertrofia",
        "organizacion": "Full Body",
        "principal_tren_superior": "Traditional Push-ups",
        "principal_tren_inferior": "Bulgarian Squats",
        "semanas_por_mesociclo": 4,
        "sesiones_por_semana": 3,
        "sesiones": [sesion_data]
    }

    # Act
    response = client.post(
        '/api/mesociclos', json=mesociclo_data,  follow_redirects=True).get_json()

    # Assert
    mesociclo = Mesociclo.query.first()

    assert mesociclo.usuario.username == "usuarioprueba"
    assert mesociclo.objetivo.descripcion == "Hipertrofia"
    assert mesociclo.organizacion.descripcion == "Full Body"
    assert mesociclo.principal_tren_superior.nombre == "Traditional Push-ups"
    assert mesociclo.semanas_por_mesociclo == 4
    assert len(mesociclo.sesiones) == 1
