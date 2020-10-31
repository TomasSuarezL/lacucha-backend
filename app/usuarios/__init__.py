BASE_ROUTE = "usuarios"


def register_routes(api, app, root="api"):
    from .controller import api as usuarios_api

    api.add_namespace(usuarios_api, path=f"/{root}/{BASE_ROUTE}")
