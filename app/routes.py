def register_routes(api, app, root="api"):
    from app.ejercicios import register_routes as attach_ejercicios
    from app.bloques import register_routes as attach_bloques
    from app.sesiones import register_routes as attach_sesiones

    # Add routes
    attach_ejercicios(api, app)
    attach_sesiones(api, app)
    attach_bloques(api, app)
