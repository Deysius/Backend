from flask import Blueprint
from database import db

from models.usuario import Usuario
from models.rol_aplicacion import RolAplicacion
from models.historico_productividad import HistoricoProductividad

productividad_bp = Blueprint(
    "productividad",
    __name__
)

@productividad_bp.route(
    "/productividad",
    methods=["GET"]
)
def calcular_productividad():

    resultado = []
    usuarios = Usuario.query.all()
    reglas = RolAplicacion.query.all()

    for usuario in usuarios:
        total_productivo = 0
        total_general = 0

        for actividad in usuario.actividades:
            for regla in reglas:
                if (
                    regla.rol_id == usuario.rol_id
                    and
                    regla.aplicacion_id == actividad.aplicacion_id
                ):
                    # El tiempo base real que el usuario pasa en la sesión (Activo + Inactivo)
                    tiempo_base_sesion = actividad.tiempo_activo + actividad.tiempo_inactivo
                    
                    # =========================================================
                    # PONDERACIÓN DE PERIFÉRICOS COMO BONO CONTROLADO
                    # =========================================================
                    # Escalamos los periféricos para que aporten minutos lógicos, no miles
                    bono_clicks = min(actividad.clicks_mouse / 100, 15)
                    bono_teclas = min(actividad.teclas_presionadas / 200, 15)
                    bono_mouse = min(actividad.movimiento_mouse / 10000, 10)
                    
                    total_bonos = bono_clicks + bono_teclas + bono_mouse
                    
                    # La actividad real toma el tiempo activo en la app + los bonos de hardware
                    actividad_real = actividad.tiempo_activo + total_bonos
                    
                    # Protección: El rendimiento premiado jamás debe superar al tiempo de silla real
                    if actividad_real > tiempo_base_sesion:
                        actividad_real = tiempo_base_sesion

                    # Acumulamos en el total de la sesión
                    total_general += tiempo_base_sesion

                    # Si el rol mapea la app como productiva, sumamos el tiempo con bono
                    if regla.es_productiva:
                        total_productivo += actividad_real

        indice = 0
        if total_general > 0:
            indice = (
                total_productivo
                /
                total_general
            ) * 100

        resultado.append({
            "usuario": usuario.nombre,
            "rol": usuario.rol.nombre if usuario.rol else "Sin Rol",
            "total_productivo": round(total_productivo, 2),
            "total_general": round(total_general, 2),
            "indice_productividad": round(indice, 2)
        })

        # ============================================================
        # 🟢 CAMBIO DE SEGURIDAD: Solo guarda si el usuario registra actividad
        # ============================================================
        if total_general > 0:
            existe = HistoricoProductividad.query.filter_by(
                usuario_id=usuario.id,
                periodo="2026-06"
            ).first()

            if not existe:
                historico = HistoricoProductividad(
                    periodo="2026-06",
                    indice_productividad=round(indice, 2),
                    usuario_id=usuario.id
                )
                db.session.add(historico)
        # ============================================================

    db.session.commit()
    return resultado