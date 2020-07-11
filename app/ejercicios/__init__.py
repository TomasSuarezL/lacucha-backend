from .model import Ejercicio

BASE_ROUTE = "ejercicios"


def register_routes(api, app, root="api"):
    from .controller import api as ejercicios_api

    api.add_namespace(ejercicios_api, path=f"/{root}/{BASE_ROUTE}")
