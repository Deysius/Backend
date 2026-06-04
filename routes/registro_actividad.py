from flask import Blueprint, request
from database import db
from models.registro_actividad import RegistroActividad
from datetime import datetime

actividad_bp = Blueprint(
    "actividad",
    __name__
)

@actividad_bp.route(
    "/actividad",
    methods=["GET"]
)
def obtener_actividad():

    actividades = RegistroActividad.query.all()

    resultado = []

    for actividad in actividades:

        resultado.append({

            "id": actividad.id,

            "usuario_id": actividad.usuario_id,

            "aplicacion_id": actividad.aplicacion_id,

            "tiempo_activo": actividad.tiempo_activo,

            "tiempo_inactivo": actividad.tiempo_inactivo,

            "clicks_mouse": actividad.clicks_mouse,

            "teclas_presionadas": actividad.teclas_presionadas,

            "movimiento_mouse": actividad.movimiento_mouse

        })

    return resultado


@actividad_bp.route(
    "/actividad",
    methods=["POST"]
)
def crear_actividad():

    data = request.json

    actividad = RegistroActividad(

        fecha=datetime.strptime(
            data["fecha"],
            "%Y-%m-%d"
        ),

        tiempo_activo=data["tiempo_activo"],

        tiempo_inactivo=data["tiempo_inactivo"],

        clicks_mouse=data["clicks_mouse"],

        teclas_presionadas=data["teclas_presionadas"],

        movimiento_mouse=data["movimiento_mouse"],

        usuario_id=data["usuario_id"],

        aplicacion_id=data["aplicacion_id"]
    )

    db.session.add(actividad)

    db.session.commit()

    return {
        "mensaje": "Actividad registrada"
    }