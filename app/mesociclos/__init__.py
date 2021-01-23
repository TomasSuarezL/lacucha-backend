BASE_ROUTE = "mesociclos"


def register_routes(api, app, root="api"):
    from .controller import api as mesociclos_api

    api.add_namespace(mesociclos_api, path=f"/{root}/{BASE_ROUTE}")
