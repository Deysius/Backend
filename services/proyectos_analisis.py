from flask import Blueprint

from models.proyecto import Proyecto

analisis_proyecto_bp = Blueprint(
    "analisis_proyecto",
    __name__
)

@analisis_proyecto_bp.route(
    "/analisis-proyectos",
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

        estado = "En Progreso"

        if porcentaje >= 100:

            estado = "Completado"

        elif porcentaje < 50:

            estado = "Atrasado"

        resultado.append({

            "proyecto":
            proyecto.nombre,

            "horas_estimadas":
            proyecto.horas_estimadas,

            "horas_reales":
            horas_reales,

            "porcentaje":
            round(porcentaje, 2),

            "estado":
            estado

        })

    return resultado