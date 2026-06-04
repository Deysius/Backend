from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.usuario import Usuario
from models.meta import Meta
from models.proyecto import Proyecto
from models.plan_mejora import PlanMejora
from models.historico_productividad import HistoricoProductividad

plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plan-mejora", methods=["GET"])
@jwt_required()
def generar_plan():
    usuario_id = int(get_jwt_identity())
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    recomendaciones = []

    # 1. Evaluación de Históricos
    historicos = HistoricoProductividad.query.filter_by(usuario_id=usuario_id).order_by(HistoricoProductividad.periodo.asc()).all()
    if len(historicos) >= 2:
        ultimo, anterior = historicos[-1], historicos[-2]
        if ultimo.indice_productividad < anterior.indice_productividad:
            recomendaciones.append(f"Tu productividad disminuyó de {anterior.indice_productividad}% a {ultimo.indice_productividad}%.")

    # 2. Evaluación de Proyectos
    for proyecto in usuario.proyectos:
        horas_reales = sum(a.horas_trabajadas for a in proyecto.avances)
        if horas_reales < (proyecto.horas_estimadas * 0.5):
            recomendaciones.append(f"Incrementar dedicación al proyecto '{proyecto.nombre}'. Progreso: {horas_reales}h de {proyecto.horas_estimadas}h.")

    # 3. Evaluación de Metas
    metas = Meta.query.filter_by(usuario_id=usuario_id).all()
    if metas:
        for meta in metas:
            progreso = meta.progreso or 0.0
            if progreso < (meta.objetivo * 0.5):
                recomendaciones.append(f"Revisar meta '{meta.titulo}'. Progreso actual: {progreso}/{meta.objetivo}.")
    else:
        recomendaciones.append("Configura tus metas de productividad en el panel principal.")

    # 4. Sincronización (Limpiar y guardar solo para este usuario)
    PlanMejora.query.filter_by(usuario_id=usuario_id).delete()
    for rec in recomendaciones:
        db.session.add(PlanMejora(recomendacion=rec, estado="Pendiente", usuario_id=usuario_id))
    
    db.session.commit()

    # 5. Respuesta
    planes = PlanMejora.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([{
        "id": p.id,
        "recomendacion": p.recomendacion,
        "estado": p.estado
    } for p in planes])