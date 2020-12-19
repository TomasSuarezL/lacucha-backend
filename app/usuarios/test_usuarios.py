from app.conftest import create_mesociclo_db, create_usuario_db
from app.usuarios.model import Genero, Nivel, Usuario
from datetime import datetime, timedelta
from dateutil import parser

# Service


def test_crear_usuario_valido(db):
    # Arrange
    genero = db.session.query(Genero).first()
    nivel = db.session.query(Nivel).first()

    # Act

    user = Usuario(
        username="usuarioprueba",
        email="usuario@prueba.com",
        nombre="Usuario",
        apellido="Prueba",
        fecha_nacimiento=datetime(1989, 8, 22),
        genero=genero,
        altura=1.77,
        peso=68,
        nivel=nivel,
    )

    db.session.add(user)
    db.session.commit()

    # Assert
    assert user.username == "usuarioprueba"


# Controller
def test_get_proxima_sesion_usuario(db, client):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    usuario = Usuario.query.get(1)

    # Act
    response = client.get(
        f'/api/usuarios/{usuario.id_usuario}/mesociclos/proximaSesion',  follow_redirects=True).get_json()

    # Assert
    assert response != None
    assert parser.parse(
        response['fechaEmpezado']).date() == datetime.utcnow().date()
    assert len(response['bloques']) == 2


def test_get_sesion_hoy_usuario(db, client):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    usuario = Usuario.query.get(1)

    # Act
    response = client.get(
        f'/api/usuarios/{usuario.id_usuario}/mesociclos/sesionHoy',  follow_redirects=True).get_json()

    # Assert
    assert response != None
    assert parser.parse(
        response['fechaEmpezado']).date() == datetime.utcnow().date()
    assert len(response['bloques']) == 2
