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
def test_get_usuarios_search(db, client, token):
    ## This will test a couple of cases, correct and incorrect. This is not ideal, but I decided that the test is so simple that is
    ## unnecesary to recreate db and request new tokens for each case, and putting them all together was better.

    # Arrange
    create_usuario_db(db)
    search_good = "Usua"  # Partial name of the user created in create_usuario_db
    search_bad = "User"  # This name shouldn't exist on db

    # Act
    response_good = client.get(
        f"/api/usuarios?search={search_good}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()
    response_bad = client.get(
        f"/api/usuarios?search={search_bad}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    assert response_good != None
    assert len(response_good) == 1
    assert response_good[0]["nombre"] == "Usuario"

    assert response_bad != None
    assert len(response_bad) == 0


def test_get_proxima_sesion_usuario(db, client):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    usuario = Usuario.query.get(1)

    # Act
    response = client.get(
        f"/api/usuarios/{usuario.id_usuario}/mesociclos/proximaSesion",
        follow_redirects=True,
    ).get_json()

    # Assert
    assert response != None
    assert parser.parse(response["fechaEmpezado"]).date() == datetime.utcnow().date()
    assert len(response["bloques"]) == 2


def test_get_sesion_hoy_usuario(db, client):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    usuario = Usuario.query.get(1)

    # Act
    response = client.get(
        f"/api/usuarios/{usuario.id_usuario}/mesociclos/sesionHoy",
        follow_redirects=True,
    ).get_json()

    # Assert
    assert response != None
    assert parser.parse(response["fechaEmpezado"]).date() == datetime.utcnow().date()
    assert len(response["bloques"]) == 2


def test_crear_usuario(db, client):
    # Arrange
    usuario_body = {
        "username": "usertest",
        "email": "user@email.test",
        "nombre": "User",
        "apellido": "Test",
    }

    # Act
    response = client.post(
        f"/api/usuarios", json=usuario_body, follow_redirects=True
    ).get_json()

    # Assert
    usuario = Usuario.query.filter_by(username="usertest").first()

    assert response != None
    assert usuario.email == "user@email.test"
    assert usuario.nombre == "User"
