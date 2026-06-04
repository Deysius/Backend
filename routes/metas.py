from flask import Blueprint, request, jsonify
from database import db
from models.meta import Meta
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

metas_bp = Blueprint(
    "metas",
    __name__
)

# ============================================================
# 1. CREAR META
# ============================================================
@metas_bp.route(
    "/metas",
    methods=["POST"]
)
@jwt_required()
def crear_meta():
    usuario_id = int(get_jwt_identity())
    data = request.json

    print("DATA RECIBIDA:", data)

    titulo = data.get("titulo")
    objetivo = data.get("objetivo")
    prioridad = data.get("prioridad")

    print("titulo =", titulo)
    print("objetivo =", objetivo)
    print("prioridad =", prioridad)

    # VALIDACIONES
    if not titulo:
        return jsonify({
            "error": "El título es obligatorio"
        }), 400

    if not objetivo:
        return jsonify({
            "error": "El objetivo es obligatorio"
        }), 400

    if objetivo <= 0:
        return jsonify({
            "error": "El objetivo debe ser mayor a 0"
        }), 400

    if prioridad not in ["Alta", "Media", "Baja"]:
        return jsonify({
            "error": "Prioridad inválida"
        }), 400

    nueva_meta = Meta(
        titulo=titulo,
        objetivo=objetivo,
        prioridad=prioridad,
        usuario_id=usuario_id
    )

    db.session.add(nueva_meta)
    db.session.commit()

    return jsonify({
        "message": "Meta creada correctamente"
    })


# ============================================================
# 2. OBTENER METAS
# ============================================================
@metas_bp.route(
    "/metas",
    methods=["GET"]
)
def obtener_metas():
    usuario_id = 1
    metas = Meta.query.filter_by(usuario_id=usuario_id).all()

    resultado = []

    for meta in metas:
        # Validación preventiva: si progreso es None en BD, lo tratamos como 0
        progreso_actual = meta.progreso if meta.progreso is not None else 0
        
        porcentaje = (progreso_actual / meta.objetivo) * 100

        resultado.append({
            "id": meta.id,
            "titulo": meta.titulo,
            "objetivo": meta.objetivo,
            "progreso": progreso_actual,
            "prioridad": meta.prioridad,
            "avance": round(porcentaje, 2)
        })

    return jsonify(resultado)


# ============================================================
# 3. ACTUALIZAR PROGRESO DE UNA META (NUEVO ENDPOINT)
# ============================================================
@metas_bp.route(
    "/metas/<int:meta_id>/progreso",
    methods=["PUT"]
)
def actualizar_progreso_meta(meta_id):
    data = request.json
    
    # Recibimos cuántos puntos le vas a sumar al progreso actual
    progreso_a_sumar = data.get("progreso")

    if progreso_a_sumar is None:
        return jsonify({
            "error": "El valor de progreso a sumar es obligatorio"
        }), 400

    # Buscamos la meta específica por su ID único de base de datos
    meta = Meta.query.get(meta_id)

    if not meta:
        return jsonify({
            "error": "Meta no encontrada"
        }), 404

    # Aseguramos que el valor inicial no sea None antes de operar aritméticamente
    if meta.progreso is None:
        meta.progreso = 0.0

    # Sumamos el avance reportado por el usuario
    meta.progreso += float(progreso_a_sumar)
    
    # Restricción lógica: El progreso no puede ser mayor que la meta fijada
    if meta.progreso > meta.objetivo:
        meta.progreso = meta.objetivo

    db.session.commit()

    return jsonify({
        "message": "Progreso de la meta actualizado con éxito",
        "nuevo_progreso": meta.progreso,
        "objetivo": meta.objetivo
    })