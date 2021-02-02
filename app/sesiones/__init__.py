BASE_ROUTE = "sesiones"


def register_routes(api, app, root="api"):
    from .controller import api as sesiones_api

    api.add_namespace(sesiones_api, path=f"/{root}/{BASE_ROUTE}")
