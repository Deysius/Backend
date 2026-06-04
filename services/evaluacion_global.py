from flask import Blueprint, jsonify
from models.usuario import Usuario
from models.proyecto import Proyecto
from models.rol_aplicacion import RolAplicacion
from models.historico_productividad import HistoricoProductividad  # <-- IMPORTANTE PARA LEER LOS HISTÓRICOS

evaluacion_bp = Blueprint("evaluacion", __name__)

@evaluacion_bp.route("/evaluacion-global", methods=["GET"])
def evaluacion_global():
    resultado = []
    usuarios = Usuario.query.all()
    regles = RolAplicacion.query.all()

    for usuario in usuarios:
        productividad = 0

        # ============================================================
        # 1. CALCULAR PRODUCTIVIDAD USANDO EL ÚLTIMO HISTÓRICO
        # ============================================================
        # Buscamos el histórico más reciente (ordenado de forma descendente por periodo)
        ultimo_historico = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
        ).order_by(HistoricoProductividad.periodo.desc()).first()

        if ultimo_historico:
            # Si el usuario tiene históricos (como tu nuevo registro de 10%), toma ese valor directo
            productividad = ultimo_historico.indice_productividad
        else:
            # BLINDAJE: Si es un usuario nuevo sin históricos, calcula usando actividades en vivo como respaldo
            total_general = 0
            total_productivo = 0
            for actividad in usuario.actividades:
                for regla in regles:
                    if (regla.rol_id == usuario.rol_id and regla.aplicacion_id == actividad.aplicacion_id):
                        total_general += actividad.tiempo_activo
                        if regla.es_productiva:
                            total_productivo += actividad.tiempo_activo
            if total_general > 0:
                productividad = (total_productivo / total_general) * 100

        # ============================================================
        # 2. CALCULAR AVANCE DE PROYECTOS
        # ============================================================
        avance_promedio = 0
        proyectos = Proyecto.query.filter_by(usuario_id=usuario.id).all()

        if proyectos:
            suma_avances = 0
            for proyecto in proyectos:
                horas_reales = 0
                for avance in proyecto.avances:
                    horas_reales += avance.horas_trabajadas

                if proyecto.horas_estimadas > 0:
                    porcentaje_proy = (horas_reales / proyecto.horas_estimadas) * 100
                    suma_avances += min(porcentaje_proy, 100)

            avance_promedio = suma_avances / len(proyectos)

        # ============================================================
        # 3. DETERMINAR CONCLUSIÓN
        # ============================================================
      # ============================================================
        # 3. DETERMINAR CONCLUSIÓN (Optimizado por Rangos Globales)
        # ============================================================
        # Sacamos el promedio real de tu rendimiento
        nota_global = (productividad + avance_promedio) / 2
        
        if nota_global >= 85:
            conclusion = "Excelente desempeño general"
        elif nota_global >= 70:
            conclusion = "Rendimiento altamente eficiente"
        elif nota_global >= 50:
            conclusion = "Rendimiento equilibrado"
        else:
            conclusion = "Alerta: Requiere optimización urgente de procesos"
        resultado.append({
            "usuario": usuario.nombre,
            "productividad": round(productividad, 2),
            "avance_proyectos": round(avance_promedio, 2),
            "conclusion": conclusion
        })

    return jsonify(resultado)