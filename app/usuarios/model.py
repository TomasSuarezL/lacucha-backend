from typing import List
from app.bloques.model import EjercicioXBloque
from datetime import datetime
from app import db


class Nivel(db.Model):
    __tablename__ = "niveles"

    id_nivel = db.Column(db.Integer, db.Sequence(
        'niveles_id_nivel_seq'), primary_key=True, unique=True)
    descripcion = db.Column(db.String(100), unique=True)

    def __init__(self, descripcion: str):
        self.descripcion = descripcion


class Genero(db.Model):
    __tablename__ = "generos"

    id_genero = db.Column(db.Integer, db.Sequence(
        'generos_id_genero_seq'), primary_key=True, unique=True)
    descripcion = db.Column(db.String(100), unique=True)

    def __init__(self, descripcion: str):
        self.descripcion = descripcion


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, db.Sequence(
        'usuarios_id_usuario_seq'), primary_key=True, unique=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    nombre = db.Column(db.String(100), unique=True)
    apellido = db.Column(db.String(100), unique=True)
    img_url = db.Column(db.String(250), unique=True)
    fecha_nacimiento = db.Column(db.DateTime)
    id_genero = db.Column(db.Integer, db.ForeignKey(
        'generos.id_genero'))
    genero = db.relationship("Genero", uselist=False, lazy=True)
    altura = db.Column(db.Float)
    peso = db.Column(db.Float)
    id_nivel = db.Column(db.Integer, db.ForeignKey(
        'niveles.id_nivel'))
    nivel = db.relationship("Nivel", uselist=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(self,
                 username: str,
                 email: str,
                 nombre: str,
                 apellido: str,
                 fecha_nacimiento: datetime,
                 genero: Genero,
                 altura: float,
                 peso: float,
                 nivel: Nivel,
                 img_url: str
                 ):
        self.username = username
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.altura = altura
        self.peso = peso
        self.nivel = nivel
        self.img_url = img_url

    def __repr__(self):
        return '<Usuario {}>'.format(self.id_usuario)
