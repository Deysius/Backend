from flask import Blueprint, request

from database import db

from models.rol_aplicacion import RolAplicacion

rol_aplicacion_bp = Blueprint(
    "rol_aplicacion",
    __name__
)

@rol_aplicacion_bp.route(
    "/rol-aplicacion",
    methods=["GET"]
)
def obtener_relaciones():

    relaciones = RolAplicacion.query.all()

    resultado = []

    for relacion in relaciones:

        resultado.append({

            "id": relacion.id,

            "rol":
            relacion.rol_id,

            "aplicacion":
            relacion.aplicacion_id,

            "es_productiva":
            relacion.es_productiva

        })

    return resultado


@rol_aplicacion_bp.route(
    "/rol-aplicacion",
    methods=["POST"]
)
def crear_relacion():

    data = request.json

    relacion = RolAplicacion(

        rol_id=data["rol_id"],

        aplicacion_id=data["aplicacion_id"],

        es_productiva=data["es_productiva"]

    )

    db.session.add(relacion)

    db.session.commit()

    return {
        "mensaje": "Relación creada"
    }