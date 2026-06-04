from flask import Blueprint, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usuario import Usuario
from models.meta import Meta
from models.proyecto import Proyecto
from models.plan_mejora import PlanMejora
from models.historico_productividad import HistoricoProductividad

plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plan-mejora", methods=["GET"])
@jwt_required()
def generar_plan():
    # 1. Identificar usuario logueado
    usuario_id = int(get_jwt_identity()) 
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    recomendaciones = []

    # 2. EVALUACIÓN DE HISTÓRICOS
    historicos = HistoricoProductividad.query.filter_by(
        usuario_id=usuario.id
    ).order_by(HistoricoProductividad.periodo.asc()).all()

    if len(historicos) >= 2:
        ultimo = historicos[-1]
        anterior = historicos[-2]
        if ultimo.indice_productividad < anterior.indice_productividad:
            recomendaciones.append(
                f"La productividad disminuyó de {anterior.indice_productividad}% a {ultimo.indice_productividad}%."
            )

    # 3. EVALUACIÓN DE PROYECTOS
    proyectos = Proyecto.query.filter_by(usuario_id=usuario.id).all()
    for proyecto in proyectos:
        horas_reales = sum(a.horas_trabajadas for a in proyecto.avances) if proyecto.avances else 0
        if horas_reales < (proyecto.horas_estimadas * 0.5):
            recomendaciones.append(
                f"Incrementar dedicación al proyecto '{proyecto.nombre}'. Llevas {horas_reales}h de {proyecto.horas_estimadas}h."
            )

    # 4. EVALUACIÓN DE METAS
    metas_usuario = Meta.query.filter_by(usuario_id=usuario.id).all()
    if metas_usuario:
        for meta in metas_usuario:
            progreso_real = meta.progreso if meta.progreso is not None else 0.0
            if progreso_real < (meta.objetivo * 0.5):
                recomendaciones.append(
                    f"Revisar cumplimiento de meta: '{meta.titulo}'. Progreso: {progreso_real}/{meta.objetivo}."
                )
    else:
        recomendaciones.append("Configurar metas de productividad mensuales.")

    # 5. SINCRONIZACIÓN EN BD
    # Borrar recomendaciones previas del usuario y guardar las nuevas
    PlanMejora.query.filter_by(usuario_id=usuario.id).delete()
    
    for rec in recomendaciones:
        db.session.add(PlanMejora(recomendacion=rec, estado="Pendiente", usuario_id=usuario.id))
    
    db.session.commit()

    # 6. RESPUESTA FINAL
    planes_guardados = PlanMejora.query.filter_by(usuario_id=usuario.id).all()
    
    respuesta = [{
        "usuario": usuario.nombre,
        "recomendaciones": [p.recomendacion for p in planes_guardados],
        "detalles_documentados": [{
            "id": p.id,
            "recomendacion": p.recomendacion,
            "estado": p.estado
        } for p in planes_guardados]
    }]

    return jsonify(respuesta)