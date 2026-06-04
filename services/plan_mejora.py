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
    usuario_id = int(get_jwt_identity())
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    recomendaciones = []

    # 1. EVALUACIÓN DE HISTÓRICOS
    historicos = HistoricoProductividad.query.filter_by(usuario_id=usuario_id).order_by(HistoricoProductividad.periodo.asc()).all()
    if len(historicos) >= 2:
        ultimo, anterior = historicos[-1], historicos[-2]
        if ultimo.indice_productividad < anterior.indice_productividad:
            recomendaciones.append(f"Tu productividad bajó ligeramente. Intenta mantener el ritmo del periodo anterior.")
    elif len(historicos) == 1:
        recomendaciones.append("Tienes un registro de productividad inicial. ¡Sigue trabajando para ver tu evolución!")

    # 2. EVALUACIÓN DE PROYECTOS
    proyectos = Proyecto.query.filter_by(usuario_id=usuario_id).all()
    for p in proyectos:
        horas_reales = sum([a.horas_trabajadas for a in p.avances]) if p.avances else 0
        # Aumentamos el umbral al 80% para que sea más fácil recibir consejos de progreso
        if horas_reales < (p.horas_estimadas * 0.8):
            recomendaciones.append(f"Proyecto '{p.nombre}': Llevas {horas_reales}h de {p.horas_estimadas}h. ¡Mantén el enfoque!")
        else:
            recomendaciones.append(f"¡Buen avance en el proyecto '{p.nombre}'! Estás cerca de la meta.")

    # 3. EVALUACIÓN DE METAS
    metas = Meta.query.filter_by(usuario_id=usuario_id).all()
    if metas:
        for m in metas:
            progreso = m.progreso or 0.0
            if progreso < m.objetivo:
                recomendaciones.append(f"Meta '{m.titulo}': Progreso actual {progreso}/{m.objetivo}. ¡Vamos por más!")
            else:
                recomendaciones.append(f"¡Felicidades! Has completado la meta '{m.titulo}'.")
    else:
        recomendaciones.append("Aún no tienes metas configuradas. Crea algunas para medir mejor tu éxito.")

    # 4. SINCRONIZACIÓN
    PlanMejora.query.filter_by(usuario_id=usuario_id).delete()
    for rec in recomendaciones:
        db.session.add(PlanMejora(recomendacion=rec, estado="Pendiente", usuario_id=usuario_id))
    db.session.commit()

    return jsonify([{
        "id": p.id,
        "recomendacion": p.recomendacion,
        "estado": p.estado
    } for p in PlanMejora.query.filter_by(usuario_id=usuario_id).all()])