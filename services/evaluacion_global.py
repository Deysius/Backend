from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usuario import Usuario
from models.proyecto import Proyecto
from models.rol_aplicacion import RolAplicacion
from models.historico_productividad import HistoricoProductividad

evaluacion_bp = Blueprint("evaluacion", __name__)

@evaluacion_bp.route("/evaluacion-global", methods=["GET"])
@jwt_required()  # <--- PROTEGIDO: Solo el usuario logueado puede acceder
def evaluacion_global():
    usuario_id = int(get_jwt_identity())
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # 1. CALCULAR PRODUCTIVIDAD
    productividad = 0.0
    ultimo_historico = HistoricoProductividad.query.filter_by(
        usuario_id=usuario_id
    ).order_by(HistoricoProductividad.periodo.desc()).first()

    if ultimo_historico:
        productividad = ultimo_historico.indice_productividad
    else:
        # Respaldo con actividades si no hay históricos
        regles = RolAplicacion.query.all()
        total_general = sum(a.tiempo_activo for a in usuario.actividades)
        total_productivo = sum(
            a.tiempo_activo for a in usuario.actividades 
            for r in regles if r.rol_id == usuario.rol_id and r.aplicacion_id == a.aplicacion_id and r.es_productiva
        )
        if total_general > 0:
            productividad = (total_productivo / total_general) * 100

    # 2. CALCULAR AVANCE DE PROYECTOS
    proyectos = Proyecto.query.filter_by(usuario_id=usuario_id).all()
    suma_avances = 0
    if proyectos:
        for p in proyectos:
            horas_reales = sum(a.horas_trabajadas for a in p.avances)
            porcentaje_proy = (horas_reales / p.horas_estimadas * 100) if p.horas_estimadas > 0 else 0
            suma_avances += min(porcentaje_proy, 100)
        avance_promedio = suma_avances / len(proyectos)
    else:
        avance_promedio = 0

    # 3. DETERMINAR CONCLUSIÓN
    nota_global = (productividad + avance_promedio) / 2
    
    if nota_global >= 85: conclusion = "Excelente desempeño general"
    elif nota_global >= 70: conclusion = "Rendimiento altamente eficiente"
    elif nota_global >= 50: conclusion = "Rendimiento equilibrado"
    else: conclusion = "Alerta: Requiere optimización urgente de procesos"

    return jsonify({
        "usuario": usuario.nombre,
        "productividad": round(productividad, 2),
        "avance_proyectos": round(avance_promedio, 2),
        "conclusion": conclusion
    })