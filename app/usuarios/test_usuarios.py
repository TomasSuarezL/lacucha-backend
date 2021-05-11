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
    search_good_nombre = "Usua"  # Partial name of the user created in create_usuario_db
    search_bad_nombre = "User"  # This name shouldn't exist on db

    # Act
    response_good_nombre = client.get(
        f"/api/usuarios?search={search_good_nombre}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()
    response_bad_nombre = client.get(
        f"/api/usuarios?search={search_bad_nombre}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    search_good_apellido = (
        "Prue"  # Partial surname of the user created in create_usuario_db
    )
    search_bad_apellido = "Prun"  # This apellido shouldn't exist on db

    # Act
    response_good_apellido = client.get(
        f"/api/usuarios?search={search_good_apellido}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()
    response_bad_apellido = client.get(
        f"/api/usuarios?search={search_bad_apellido}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    search_good_email = (
        "rio@pr"  # Partial email of the user created in create_usuario_db
    )
    search_bad_email = "fafa"  # This email shouldn't exist on db

    # Act
    response_good_email = client.get(
        f"/api/usuarios?search={search_good_email}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()
    response_bad_email = client.get(
        f"/api/usuarios?search={search_bad_email}",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    assert None not in (
        response_good_nombre,
        response_good_apellido,
        response_good_email,
    )
    assert 1 in {
        len(response_good_nombre),
        len(response_good_apellido),
        len(response_good_email),
    }
    assert "Usuario" in {
        response_good_nombre[0]["nombre"],
        response_good_apellido[0]["nombre"],
        response_good_email[0]["nombre"],
    }

    assert None not in (response_bad_nombre, response_bad_apellido, response_bad_email)
    assert 0 in {
        len(response_bad_nombre),
        len(response_bad_apellido),
        len(response_bad_email),
    }


def test_controller_get_valid_mesociclo(db, client, token):
    # Arrange
    create_usuario_db(db)
    create_mesociclo_db(db)

    # Act
    mesociclo = client.get(
        f"/api/usuarios/{1}/mesociclos?activo=False",
        follow_redirects=True,
        headers={"Authorization": f"Bearer {token}"},
    ).get_json()

    # Assert
    assert mesociclo[0]["idMesociclo"] == 1
    assert mesociclo[0]["usuario"]["username"] == "usuarioprueba"
    assert mesociclo[0]["estado"]["descripcion"] == "Activo"
    assert mesociclo[0]["objetivo"]["descripcion"] == "Acondicionamiento General"
    assert mesociclo[0]["organizacion"]["idOrganizacion"] == 1
    assert mesociclo[0]["principalTrenInferior"]["nombre"] == "Bulgarian Squats"
    assert mesociclo[0]["semanasPorMesociclo"] == 4
    assert len(mesociclo[0]["sesiones"]) == 2


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
