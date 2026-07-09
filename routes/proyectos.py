from flask import Blueprint, request
from database import db
from models.proyecto import Proyecto
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from services.proyecto_factory import ProyectoFactory

proyectos_bp = Blueprint(
    "proyectos",
    __name__
)


# ==========================
# OBTENER PROYECTOS
# ==========================

@proyectos_bp.route(
    "/proyectos",
    methods=["GET"]
)
@jwt_required()
def obtener_proyectos():

    usuario_id = int(get_jwt_identity())

    proyectos = Proyecto.query.filter_by(
        usuario_id=usuario_id
    ).all()

    resultado = []

    for proyecto in proyectos:

        resultado.append({

            "id": proyecto.id,

            "nombre": proyecto.nombre,

            "descripcion": proyecto.descripcion,

            "horas_estimadas": proyecto.horas_estimadas,

            "prioridad": proyecto.prioridad,

            "estado": proyecto.estado,

            "usuario_id": proyecto.usuario_id

        })

    return resultado


# ==========================
# CREAR PROYECTO
# ==========================

@proyectos_bp.route(
    "/proyectos",
    methods=["POST"]
)
@jwt_required()
def crear_proyecto():

    usuario_id = int(get_jwt_identity())

    data = request.json

    proyecto = ProyectoFactory.crear_proyecto(

        nombre=data["nombre"],

        descripcion=data["descripcion"],

        fecha_inicio=datetime.strptime(
            data["fecha_inicio"],
            "%Y-%m-%d"
        ),

        fecha_fin=datetime.strptime(
            data["fecha_fin"],
            "%Y-%m-%d"
        ),

        horas_estimadas=data["horas_estimadas"],

        usuario_id=usuario_id

    )

    db.session.add(proyecto)

    db.session.commit()

    return {

        "mensaje": "Proyecto creado correctamente"

    }, 201