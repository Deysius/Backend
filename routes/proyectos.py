from flask import Blueprint, request
from database import db
from models.proyecto import Proyecto
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

proyectos_bp = Blueprint(
    "proyectos",
    __name__
)

@proyectos_bp.route(
    "/proyectos",
    methods=["GET"]
)
@jwt_required()
def obtener_proyectos():
    
    usuario_id = int(get_jwt_identity())

    proyectos = Proyecto.query.all()

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


@proyectos_bp.route(
    "/proyectos",
    methods=["POST"]
)
def crear_proyecto():

    data = request.json

    proyecto = Proyecto(
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
        prioridad=data["prioridad"],
        estado=data["estado"],
        usuario_id=data["usuario_id"]
    )

    db.session.add(proyecto)
    db.session.commit()

    return {
        "mensaje": "Proyecto creado"
    }