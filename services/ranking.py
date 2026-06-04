from flask import Blueprint

from models.usuario import Usuario
from models.historico_productividad import HistoricoProductividad

ranking_bp = Blueprint(
    "ranking",
    __name__
)
@ranking_bp.route(
    "/ranking",
    methods=["GET"]
)
def ranking():

    resultado = []

    usuarios = Usuario.query.all()

    for usuario in usuarios:

        historicos = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
        ).all()

        promedio = 0

        if historicos:

            suma = 0

            for h in historicos:

                suma += h.indice_productividad

            promedio = suma / len(historicos)

        resultado.append({

            "usuario":
            usuario.nombre,

            "promedio":
            round(promedio, 2)

        })

    resultado.sort(
        key=lambda x: x["promedio"],
        reverse=True
    )

    return resultado