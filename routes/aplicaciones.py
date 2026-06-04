from flask import Blueprint, request

from database import db

from models.aplicacion import Aplicacion

aplicaciones_bp = Blueprint(
    "aplicaciones",
    __name__
)

@aplicaciones_bp.route(
    "/aplicaciones",
    methods=["GET"]
)
def obtener_aplicaciones():

    aplicaciones = Aplicacion.query.all()

    resultado = []

    for app in aplicaciones:

        resultado.append({

            "id": app.id,

            "nombre": app.nombre

        })

    return resultado


@aplicaciones_bp.route(
    "/aplicaciones",
    methods=["POST"]
)
def crear_aplicacion():

    data = request.json

    if not data.get("nombre"):

        return {
            "error": "Nombre requerido"
        }, 400

    existe = Aplicacion.query.filter_by(
        nombre=data["nombre"]
    ).first()

    if existe:

        return {
            "error": "La aplicación ya existe"
        }, 400

    app = Aplicacion(

        nombre=data["nombre"]

    )

    db.session.add(app)

    db.session.commit()

    return {
        "mensaje": "Aplicación creada"
    }, 201