from app.usuarios.model import Nivel, Usuario
from app.sesiones.model import Sesion
from app.ejercicios.model import Ejercicio
from app.bloques.model import Bloque, EjercicioXBloque
from app.mesociclos.model import Mesociclo, Objetivo
import pytest
from marshmallow.exceptions import ValidationError
from app.mesociclos.service import MesocicloService
from app.conftest import create_mesociclo_db, create_usuario_db
from datetime import datetime, timedelta


# Service
def test_crear_mesociclo_valido(db):
    # Arrange
    create_usuario_db(db)

    ej_x_bloque = EjercicioXBloque(ejercicio=Ejercicio(
        "Traditional Push-ups"), repeticiones=10, carga=20.1)

    bloque = Bloque(ejercicios=[ej_x_bloque], num_bloque=1, series=4)

    sesion = Sesion(fecha_empezado=str(datetime.utcnow()), fecha_finalizado=str(
        datetime.utcnow() + timedelta(hours=1)), bloques=[bloque])

    mesociclo = Mesociclo(usuario=Usuario.query.first(),
                          nivel=Nivel.query.first(),
                          objetivo=Objetivo.query.first(),
                          organizacion=2,
                          principal_tren_inferior=5,
                          principal_tren_superior=2,
                          semanas_por_mesociclo=4,
                          sesiones_por_semana=3,
                          sesiones=[sesion])

    # Act
    mesociclo = MesocicloService.create_mesociclo(mesociclo)

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
def test_controller_create_valid_mesociclo(db, client):
    # Arrange
    create_usuario_db(db)
    sesion_data = {"fechaEmpezado": str(datetime.utcnow()),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Pull-ups"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    mesociclo_data = {
        "usuario": {"idUsuario": 1},
        "nivel": {"idNivel": 2},
        "objetivo": {"idObjetivo": 3},
        "organizacion": {"idOrganizacion": 3},
        "principalTrenSuperior": {"idEjercicio": 2},
        "principalTrenInferior": {"idEjercicio": 5},
        "semanasPorMesociclo": 4,
        "sesionesPorSemana": 3,
        "sesiones": [sesion_data]
    }

    # Act
    response = client.post(
        '/api/mesociclos', json=mesociclo_data,  follow_redirects=True).get_json()

    # Assert
    mesociclo = Mesociclo.query.first()

    assert mesociclo.usuario.username == "usuarioprueba"
    assert mesociclo.objetivo.descripcion == "Fuerza"
    assert mesociclo.organizacion.descripcion == "Combinado"
    assert mesociclo.principal_tren_superior.nombre == "Diamond Push-ups"
    assert mesociclo.principal_tren_inferior.nombre == "Bulgarian Squats"
    assert mesociclo.estado.descripcion == "Activo"
    assert mesociclo.semanas_por_mesociclo == 4
    assert len(mesociclo.sesiones) == 1
    assert len(mesociclo.sesiones[0].bloques) == 1
    assert len(mesociclo.sesiones[0].bloques[0].ejercicios) == 1
    assert mesociclo.sesiones[0].bloques[0].ejercicios[0].ejercicio.patron.nombre == "Tren Superior"
    assert mesociclo.fecha_fin_real == None
    assert mesociclo.sentimiento == None


def test_controller_update_valid_mesociclo(db, client):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    id_mesociclo = 1

    mesociclo_data = {
        "idMesociclo": 1,
        "usuario": {"idUsuario": 1},
        "estado": {"idEstadoMesociclo": 2},
        "objetivo": {"idObjetivo": 3},
        "principalTrenSuperior": {"idEjercicio": 2},
        "principalTrenInferior": {"idEjercicio": 5},
        "fechaFinReal": str(datetime.utcnow()),
        "aumentoMotivacion": "True",
        "masCercaObjetivos": "False",
        "sentimiento": 2,
        "durmiendo": 3,
        "alimentado": 4
    }

    # Act
    response = client.put(
        f'/api/mesociclos/{id_mesociclo}', json=mesociclo_data,  follow_redirects=True).get_json()

    # Assert
    mesociclo = Mesociclo.query.first()

    assert mesociclo.id_mesociclo == 1
    assert mesociclo.usuario.username == "usuarioprueba"
    assert mesociclo.estado.descripcion == "Terminado"
    assert mesociclo.objetivo.descripcion == "Fuerza"
    assert mesociclo.organizacion.descripcion == "Full Body"
    assert mesociclo.principal_tren_superior.nombre == "Diamond Push-ups"
    assert mesociclo.principal_tren_inferior.nombre == "Bulgarian Squats"
    assert mesociclo.semanas_por_mesociclo == 4
    assert len(mesociclo.sesiones) == 1
    assert len(mesociclo.sesiones[0].bloques) == 2
    assert len(mesociclo.sesiones[0].bloques[0].ejercicios) == 3
    assert mesociclo.sesiones[0].bloques[0].ejercicios[0].ejercicio.patron.nombre == "Tren Superior"
    assert mesociclo.fecha_fin_real != None
    assert mesociclo.sentimiento == 2
    assert mesociclo.aumento_motivacion
    assert not mesociclo.mas_cerca_objetivos
    assert mesociclo.alimentado == 4
    assert mesociclo.actualizado_en.date() == datetime.utcnow().date()


def test_controller_get_valid_mesociclo(db, client):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)
    mesociclo_id = 1

    # Act
    mesociclo = client.get(
        f'/api/mesociclos/{mesociclo_id}',  follow_redirects=True).get_json()

    # Assert
    assert mesociclo["id_mesociclo"] == 1
    assert mesociclo["usuario"]["username"] == "usuarioprueba"
    assert mesociclo["estado"]["descripcion"] == "Activo"
    assert mesociclo["objetivo"]["descripcion"] == "Acondicionamiento General"
    assert mesociclo["organizacion"]["id_organizacion"] == 1
    assert mesociclo["principal_tren_inferior"]["nombre"] == "Bulgarian Squats"
    assert mesociclo["semanas_por_mesociclo"] == 4
    assert len(mesociclo["sesiones"]) == 0
