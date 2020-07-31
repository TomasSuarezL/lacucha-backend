from app.conftest import create_ejercicio_db
from app.bloques.model import Bloque, EjercicioXBloque
from app.ejercicios.model import Ejercicio
from app.sesiones.model import Sesion
from app.sesiones.service import SesionService
from datetime import datetime, timedelta


def test_crear_sesion(db):
    sesion_data = {"empezado": str(datetime.utcnow()),
                   "finalizado": str(datetime.utcnow() + timedelta(hours=1)),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Ejercicio"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    create_ejercicio_db(db)

    SesionService.create_sesion(sesion_data)

    sesiones = Sesion.query.all()

    assert len(sesiones) == 1
