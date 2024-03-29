from marshmallow.fields import Nested, Pluck
from marshmallow.utils import EXCLUDE
from app.usuarios.model import Genero, Nivel, Usuario
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app import db


class GeneroSchema(SQLAlchemySchema):
    class Meta:
        model = Genero
        load_instance = True

    idGenero = auto_field("id_genero")
    descripcion = auto_field()


class NivelSchema(SQLAlchemySchema):
    class Meta:
        model = Nivel
        load_instance = True

    idNivel = auto_field("id_nivel")
    descripcion = auto_field()


class UsuarioSchema(SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True  # Optional: deserialize to model instances
        unknown = EXCLUDE

    idUsuario = auto_field("id_usuario")
    uuid = auto_field()
    username = auto_field()
    email = auto_field()
    nombre = auto_field()
    apellido = auto_field()
    fechaNacimiento = auto_field("fecha_nacimiento")
    genero = Nested(GeneroSchema(session=db.session))
    altura = auto_field()
    peso = auto_field()
    nivel = Nested(NivelSchema(session=db.session))
    imgUrl = auto_field("img_url")
    rol = auto_field()
    creadoEn = auto_field("creado_en", dump_only=True)
    bajaEn = auto_field("baja_en", dump_only=True)
    actualizadoEn = auto_field("actualizado_en", dump_only=True)
