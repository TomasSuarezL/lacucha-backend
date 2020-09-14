from app.usuarios.model import Genero, Nivel, Usuario
from datetime import datetime, timedelta


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
