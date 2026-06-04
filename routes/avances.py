from flask import Blueprint, request
from database import db
from models.avance_proyecto import AvanceProyecto
from datetime import datetime

avances_bp = Blueprint(
    "avances",
    __name__
)

@avances_bp.route(
    "/avances",
    methods=["GET"]
)
def obtener_avances():

    avances = AvanceProyecto.query.all()

    resultado = []

    for avance in avances:

        resultado.append({
            "id": avance.id,
            "proyecto_id": avance.proyecto_id,
            "horas_trabajadas": avance.horas_trabajadas,
            "descripcion": avance.descripcion
        })

    return resultado


@avances_bp.route(
    "/avances",
    methods=["POST"]
)
def crear_avance():

    data = request.json

    avance = AvanceProyecto(
        fecha=datetime.strptime(
            data["fecha"],
            "%Y-%m-%d"
        ),
        horas_trabajadas=data["horas_trabajadas"],
        descripcion=data["descripcion"],
        proyecto_id=data["proyecto_id"]
    )

    db.session.add(avance)
    db.session.commit()

    return {
        "mensaje": "Avance registrado"
    }