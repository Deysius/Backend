from flask import Blueprint, jsonify
from models.usuario import Usuario
from models.proyecto import Proyecto
from models.rol_aplicacion import RolAplicacion
from models.historico_productividad import HistoricoProductividad  
evaluacion_bp = Blueprint("evaluacion", __name__)

@evaluacion_bp.route("/evaluacion-global", methods=["GET"])
def evaluacion_global():
    resultado = []
    usuarios = Usuario.query.all()
    regles = RolAplicacion.query.all()

    for usuario in usuarios:
        productividad = 0

    
        ultimo_historico = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
        ).order_by(HistoricoProductividad.periodo.desc()).first()

        if ultimo_historico:
           
            productividad = ultimo_historico.indice_productividad
        else:
        
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