from app.conftest import create_mesociclo_db, create_sesion_db, create_usuario_db
from app.bloques.model import Bloque, EjercicioXBloque
from app.ejercicios.model import Ejercicio
from app.sesiones.model import Sesion
from app.sesiones.service import SesionService
from datetime import datetime, timedelta


# Service
def test_crear_sesion(db):
    sesion_data = {"empezado": str(datetime.utcnow()),
                   "finalizado": str(datetime.utcnow() + timedelta(hours=1)),
                   "bloques": [{"series": 10,
                                "numBloque": 1,
                                "ejercicios": [{"ejercicio": {"nombre": "Traditional Push-ups"}, "repeticiones": 10, "carga": 20.1}]}
                               ]
                   }

    sesion = SesionService.create_sesion(sesion_data)

    assert len(sesion.bloques) == 1


def test_get_sesion_de_hoy(db):
    # ARRANGE
    create_usuario_db(db)
    create_sesion_db(db)

    # ACT
    sesion_hoy = SesionService.get_today_sesion()

    # ASSERT
    assert sesion_hoy is not None
    assert len(sesion_hoy.bloques) == 2
