from flask import Blueprint

from models.usuario import Usuario
from models.historico_productividad import HistoricoProductividad

comparacion_bp = Blueprint(
    "comparacion",
    __name__
)

@comparacion_bp.route(
    "/comparacion",
    methods=["GET"]
)
def comparar():

    resultado = []

    usuarios = Usuario.query.all()

    for usuario in usuarios:

        historicos = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
        ).order_by(
            HistoricoProductividad.id
        ).all()

        if len(historicos) >= 2:

            anterior = historicos[-2]

            actual = historicos[-1]

            diferencia = (

                actual.indice_productividad

                -

                anterior.indice_productividad

            )

            tendencia = "Igual"

            if diferencia > 0:

                tendencia = "Mejorando"

            elif diferencia < 0:

                tendencia = "Empeorando"

            resultado.append({

                "usuario":
                usuario.nombre,

                "periodo_anterior":
                anterior.periodo,

                "productividad_anterior":
                anterior.indice_productividad,

                "periodo_actual":
                actual.periodo,

                "productividad_actual":
                actual.indice_productividad,

                "diferencia":
                round(diferencia, 2),

                "tendencia":
                tendencia

            })

    return resultado