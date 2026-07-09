from flask import Blueprint
from models.usuario import Usuario
from models.historico_productividad import HistoricoProductividad

promedio_bp = Blueprint(
    "promedio",
    __name__
)

@promedio_bp.route(
    "/promedio-semestral",
    methods=["GET"]
)
def promedio_semestral():

    resultado = []
    usuarios = Usuario.query.all()

    for usuario in usuarios:
        # 1. ORDENAMOS cronológicamente para garantizar que el último sea el mes más reciente
        historicos = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
            # Se requiere importar 'asc' o usar el string directo si tu ORM lo permite:
        ).order_by(HistoricoProductividad.periodo.asc()).all()

        if len(historicos) == 0:
            continue

        # El último mes registrado (el presente o el más cercano a hoy)
        ultimo = historicos[-1]
        
        # El histórico real corresponde a los meses PASADOS (excluimos el último de la suma)
        meses_pasados = historicos[:-1]

        if len(meses_pasados) > 0:
            suma = 0
            for h in meses_pasados:
                suma += h.indice_productividad
            promedio_historico = suma / len(meses_pasados)
        else:
            # Si solo hay un mes en total, su promedio histórico base es el mismo valor
            promedio_historico = ultimo.indice_productividad

        # Calculamos la ganancia o pérdida real contra su pasado
        diferencia = ultimo.indice_productividad - promedio_historico

        tendencia = "Superior al promedio"
        if diferencia < 0:
            tendencia = "Inferior al promedio"

        resultado.append({
            "usuario": usuario.nombre,
            "rol": usuario.rol.nombre if usuario.rol else "Sin Rol",
            "promedio_historico": round(promedio_historico, 2),
            "ultimo_periodo": ultimo.periodo,
            "ultimo_indice": round(ultimo.indice_productividad, 2),
            "diferencia": round(diferencia, 2),
            "tendencia": tendencia
        })

    return resultado