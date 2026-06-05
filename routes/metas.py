from flask import Blueprint, request, jsonify
from database import db
from models.meta import Meta
from flask_jwt_extended import jwt_required, get_jwt_identity

metas_bp = Blueprint("metas", __name__)


@metas_bp.route("/metas", methods=["POST"])
@jwt_required()
def crear_meta():
    usuario_id = int(get_jwt_identity())
    data = request.json

    titulo = data.get("titulo")
    objetivo = data.get("objetivo")
    prioridad = data.get("prioridad")

    if not all([titulo, objetivo, prioridad]):
        return jsonify({"error": "Datos incompletos"}), 400

    nueva_meta = Meta(
        titulo=titulo,
        objetivo=float(objetivo),
        prioridad=prioridad,
        usuario_id=usuario_id
    )

    db.session.add(nueva_meta)
    db.session.commit()

    return jsonify({"message": "Meta creada correctamente"}), 201



@metas_bp.route("/metas", methods=["GET"])
@jwt_required()
def obtener_metas():
    usuario_id = int(get_jwt_identity())
    metas = Meta.query.filter_by(usuario_id=usuario_id).all()

    resultado = []
    for meta in metas:
        progreso_actual = meta.progreso or 0.0
  
        porcentaje = (progreso_actual / meta.objetivo * 100) if meta.objetivo > 0 else 0
        
        resultado.append({
            "id": meta.id,
            "titulo": meta.titulo,
            "objetivo": meta.objetivo,
            "progreso": progreso_actual,
            "prioridad": meta.prioridad,
            "avance": round(porcentaje, 2)
        })

    return jsonify(resultado)

@metas_bp.route("/metas/<int:meta_id>/progreso", methods=["PUT"])
@jwt_required()
def actualizar_progreso_meta(meta_id):
    usuario_id = int(get_jwt_identity())
    data = request.json
    progreso_a_sumar = data.get("progreso")

    if progreso_a_sumar is None:
        return jsonify({"error": "El valor de progreso es obligatorio"}), 400

    
    meta = Meta.query.filter_by(id=meta_id, usuario_id=usuario_id).first()

    if not meta:
        return jsonify({"error": "Meta no encontrada o no autorizada"}), 404

    meta.progreso = (meta.progreso or 0.0) + float(progreso_a_sumar)
    
    # Límite
    if meta.progreso > meta.objetivo:
        meta.progreso = meta.objetivo

    db.session.commit()

    return jsonify({
        "message": "Progreso actualizado",
        "nuevo_progreso": meta.progreso
    })