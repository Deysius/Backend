from flask import Blueprint, request
from database import db
from models.historico_productividad import HistoricoProductividad

historico_bp = Blueprint(
    "historico",
    __name__
)

# GET HISTORICO

@historico_bp.route(
    "/historico",
    methods=["GET"]
)
def obtener_historico():

    registros = HistoricoProductividad.query.all()

    resultado = []

    for registro in registros:

        resultado.append({

            "id": registro.id,

            "usuario_id": registro.usuario_id,

            "periodo": registro.periodo,

            "indice_productividad":
            registro.indice_productividad

        })

    return resultado


# POST HISTORICO

@historico_bp.route(
    "/historico",
    methods=["POST"]
)
def crear_historico():

    data = request.json

    registro = HistoricoProductividad(

        periodo=data["periodo"],

        indice_productividad=
        data["indice_productividad"],

        usuario_id=data["usuario_id"]

    )

    db.session.add(registro)

    db.session.commit()

    return {
        "mensaje": "Histórico creado"
    }