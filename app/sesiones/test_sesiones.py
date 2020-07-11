from app.bloques.model import Bloque, EjercicioXBloque
from app.ejercicios.model import Ejercicio
from app.sesiones.model import Sesion
from datetime import datetime, timedelta


# def test_crear_sesion(db):

#     pushUps = db.session.query(Ejercicio).filter_by(
#         nombre="Traditional Push-ups").first()
#     assert pushUps.nombre == "Traditional Push-ups"

#     bloque1 = Bloque(ejercicios=[EjercicioXBloque(
#         ejercicio=pushUps, repeticiones=10, carga=10
#     )], num_bloque=1, series=4)

#     nuevaSesion = Sesion(bloques=[bloque1],
#                          fecha_empezado=datetime.now() +
#                          timedelta(hours=-1),
#                          fecha_finalizado=datetime.now())

#     db.session.add(nuevaSesion)
#     db.session.commit()

#     sesion = db.session.query(Sesion).get(nuevaSesion.id_sesiones)

#     assert len(sesion.bloques) == 1
#     assert sesion.bloques[0].series == 4
#     assert sesion.bloques[0].ejercicios[0].repeticiones == 10
#     assert sesion.bloques[0].ejercicios[0].ejercicio.nombre == "Traditional Push-ups"
#     assert sesion.bloques[0].ejercicios[0].ejercicio.patron.nombre == pushUps.patron.nombre
