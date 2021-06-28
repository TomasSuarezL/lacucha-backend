from .model import Plantilla, SesionXPlantilla

BASE_ROUTE = "plantillas"


def register_routes(api, app, root="api"):
    from .controller import api as plantillas_api

    api.add_namespace(plantillas_api, path=f"/{root}/{BASE_ROUTE}")
