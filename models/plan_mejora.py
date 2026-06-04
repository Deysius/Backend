from flask import Blueprint, jsonify
from database import db

from models.usuario import Usuario
from models.meta import Meta
from models.proyecto import Proyecto
from models.plan_mejora import PlanMejora
from models.historico_productividad import HistoricoProductividad

plan_bp = Blueprint(
    "plan",
    __name__
)

@plan_bp.route(
    "/plan-mejora",
    methods=["GET"]
)
def generar_plan():

    resultado = []
    usuarios = Usuario.query.all()

    for usuario in usuarios:
        recomendaciones = []

        # ============================================================
        # 1. EVALUACIÓN DE HISTÓRICOS
        # ============================================================
        historicos = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
        ).order_by(HistoricoProductividad.periodo.asc()).all()

        if len(historicos) >= 2:
            ultimo = historicos[-1]
            anterior = historicos[-2]

            if ultimo.indice_productividad < anterior.indice_productividad:
                recomendaciones.append(
                    f"La productividad disminuyó de {anterior.indice_productividad}% en {anterior.periodo} a {ultimo.indice_productividad}% en {ultimo.periodo}."
                )

        # ============================================================
        # 2. EVALUACIÓN DE PROYECTOS
        # ============================================================
        proyectos = usuario.proyectos if usuario.proyectos else Proyecto.query.filter_by(usuario_id=usuario.id).all()

        for proyecto in proyectos:
            horas_reales = 0
            for avance in proyecto.avances:
                horas_reales += avance.horas_trabajadas

            if horas_reales < (proyecto.horas_estimadas * 0.5):
                recomendaciones.append(
                    f"Incrementar dedicación al proyecto '{proyecto.nombre}'. Llevas {horas_reales}h de {proyecto.horas_estimadas}h estimadas."
                )

        # ============================================================
        # 3. EVALUACIÓN DE METAS (Validando Nulos de forma segura)
        # ============================================================
        metas_usuario = Meta.query.filter_by(usuario_id=usuario.id).all()
        
        if len(metas_usuario) > 0:
            for meta in metas_usuario:
                progreso_real = meta.progreso if meta.progreso is not None else 0.0
                
                # Si sigue por debajo del 50%, se mantiene la alerta activa
                if progreso_real < (meta.objetivo * 0.5):
                    recomendaciones.append(
                        f"Revisar cumplimiento de meta: '{meta.titulo}'. Progreso actual: {progreso_real}/{meta.objetivo}."
                    )
        else:
            recomendaciones.append("Configurar metas de productividad mensuales en el panel de Metas.")

        # ============================================================
        # 4. SINCRONIZACIÓN Y LIMPIEZA AUTOMÁTICA EN LA BD
        # ============================================================
        # [A] Borrar alertas viejas que ya NO están en la lista actual (Por ejemplo, si ya superaron el 50%)
        planes_existentes = PlanMejora.query.filter_by(usuario_id=usuario.id).all()
        for plan_bd in planes_existentes:
            if plan_bd.recomendacion not in recomendaciones:
                db.session.delete(plan_bd)

        # [B] Guardar las alertas nuevas que no existían antes
        for recomendacion in recomendaciones:
            existe = PlanMejora.query.filter_by(
                usuario_id=usuario.id,
                recomendacion=recomendacion
            ).first()

            if not existe:
                plan = PlanMejora(
                    recomendacion=recomendacion,
                    estado="Pendiente",
                    usuario_id=usuario.id
                )
                db.session.add(plan)
        
        db.session.commit()

        # ============================================================
        # 5. RESPUESTA REFRESCADA
        # ============================================================
        planes_guardados = PlanMejora.query.filter_by(usuario_id=usuario.id).all()
        
        resultado.append({
            "usuario": usuario.nombre,
            "recomendaciones": [p.recomendacion for p in planes_guardados],
            "detalles_documentados": [{
                "id": p.id,
                "recomendacion": p.recomendacion,
                "estado": p.estado
            } for p in planes_guardados]
        })

    return jsonify(resultado)