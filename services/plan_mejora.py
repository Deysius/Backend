from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.usuario import Usuario
from models.plan_mejora import PlanMejora
from models.meta import Meta
from models.proyecto import Proyecto
from models.historico_productividad import HistoricoProductividad

plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plan-mejora", methods=["GET"])
@jwt_required()
def generar_plan():
    # 1. Identificar al usuario logueado
    usuario_id = int(get_jwt_identity())
    
    # 2. Obtener datos del usuario
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    recomendaciones = []

    # ============================================================
    # EVALUACIÓN DE HISTÓRICOS
    # ============================================================
    historicos = HistoricoProductividad.query.filter_by(
        usuario_id=usuario_id
    ).order_by(HistoricoProductividad.periodo.asc()).all()

    if len(historicos) >= 2:
        ultimo = historicos[-1]
        anterior = historicos[-2]
        if ultimo.indice_productividad < anterior.indice_productividad:
            recomendaciones.append(
                f"Tu productividad disminuyó de {anterior.indice_productividad}% a {ultimo.indice_productividad}%."
            )

    # ============================================================
    # EVALUACIÓN DE PROYECTOS
    # ============================================================
    proyectos = Proyecto.query.filter_by(usuario_id=usuario_id).all()
    for proyecto in proyectos:
        horas_reales = sum([a.horas_trabajadas for a in proyecto.avances]) if proyecto.avances else 0
        if horas_reales < (proyecto.horas_estimadas * 0.5):
            recomendaciones.append(
                f"Incrementar dedicación al proyecto '{proyecto.nombre}'. Progreso: {horas_reales}h de {proyecto.horas_estimadas}h."
            )

    # ============================================================
    # EVALUACIÓN DE METAS
    # ============================================================
    metas_usuario = Meta.query.filter_by(usuario_id=usuario_id).all()
    if metas_usuario:
        for meta in metas_usuario:
            progreso = meta.progreso or 0.0
            if progreso < (meta.objetivo * 0.5):
                recomendaciones.append(
                    f"Revisar meta '{meta.titulo}'. Progreso actual: {progreso}/{meta.objetivo}."
                )
    else:
        recomendaciones.append("Configura tus metas de productividad en el panel principal.")

    # ============================================================
    # SINCRONIZACIÓN EN BD (Solo para este usuario)
    # ============================================================
    # Borramos los planes viejos del usuario
    PlanMejora.query.filter_by(usuario_id=usuario_id).delete()
    
    # Insertamos las nuevas recomendaciones
    for rec in recomendaciones:
        db.session.add(PlanMejora(
            recomendacion=rec,
            estado="Pendiente",
            usuario_id=usuario_id
        ))
    
    db.session.commit()

    # ============================================================
    # RESPUESTA
    # ============================================================
    planes = PlanMejora.query.filter_by(usuario_id=usuario_id).all()
    
    return jsonify([{
        "id": p.id,
        "recomendacion": p.recomendacion,
        "estado": p.estado
    } for p in planes])