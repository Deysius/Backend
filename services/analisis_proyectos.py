from flask import Blueprint

from models.proyecto import Proyecto

analisis_proyectos_bp = Blueprint(
    "analisis_proyectos",
    __name__
)

@analisis_proyectos_bp.route(
    "/analisis/proyectos",
    methods=["GET"]
)
def analizar_proyectos():

    resultado = []

    proyectos = Proyecto.query.all()

    for proyecto in proyectos:

        horas_reales = 0

        for avance in proyecto.avances:

            horas_reales += avance.horas_trabajadas

        porcentaje = 0

        if proyecto.horas_estimadas > 0:

            porcentaje = (
                horas_reales
                /
                proyecto.horas_estimadas
            ) * 100

        resultado.append({

            "proyecto": proyecto.nombre,

            "horas_estimadas":
            proyecto.horas_estimadas,

            "horas_reales":
            horas_reales,

            "avance":
            round(porcentaje, 2)

        })

    return resultado