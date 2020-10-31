from marshmallow.fields import Pluck
from app.usuarios.model import Genero, Nivel, Usuario
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


class GeneroSchema(SQLAlchemySchema):
    class Meta:
        model = Genero
        load_instance = True

    descripcion = auto_field()


class NivelSchema(SQLAlchemySchema):
    class Meta:
        model = Nivel
        load_instance = True

    descripcion = auto_field()


class UsuarioSchema(SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True  # Optional: deserialize to model instances

    id_usuario = auto_field()
    username = auto_field()
    email = auto_field()
    nombre = auto_field()
    apellido = auto_field()
    fecha_nacimiento = auto_field()
    genero = Pluck(GeneroSchema, 'descripcion')
    altura = auto_field()
    peso = auto_field()
    nivel = Pluck(NivelSchema, 'descripcion')
    img_url = auto_field()
    creado_en = auto_field(dump_only=True)
    actualizado_en = auto_field(dump_only=True)
