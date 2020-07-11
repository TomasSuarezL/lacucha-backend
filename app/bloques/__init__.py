from .model import Bloque, EjercicioXBloque

BASE_ROUTE = "bloques"


def register_routes(api, app, root="api"):
    from .controller import api as bloques_api

    api.add_namespace(bloques_api, path=f"/{root}/{BASE_ROUTE}")
