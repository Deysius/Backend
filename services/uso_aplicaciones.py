from flask import Blueprint, jsonify
from models.usuario import Usuario
from models.rol_aplicacion import RolAplicacion

uso_bp = Blueprint("uso", __name__)

@uso_bp.route("/uso-aplicaciones", methods=["GET"])
def uso_aplicaciones():
    resultado = []
    usuarios = Usuario.query.all()
    reglas = RolAplicacion.query.all()

    for usuario in usuarios:
        productivas = 0
        improductivas = 0

        for actividad in usuario.actividades:
            # Buscamos si la aplicación de esta actividad tiene regla para el rol del usuario
            for regla in reglas:
                if (regla.rol_id == usuario.rol_id and regla.aplicacion_id == actividad.aplicacion_id):
                    if regla.es_productiva:
                        productivas += actividad.tiempo_activo
                    else:
                        improductivas += actividad.tiempo_activo

        resultado.append({
            "usuario": usuario.nombre,
            "horas_productivas": productivas,   # Representa los minutos acumulados reales
            "horas_improductivas": improductivas # Representa los minutos acumulados reales
        })

    return jsonify(resultado)