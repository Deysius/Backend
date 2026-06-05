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
        
        historicos = HistoricoProductividad.query.filter_by(
            usuario_id=usuario.id
            
        ).order_by(HistoricoProductividad.periodo.asc()).all()

        if len(historicos) == 0:
            continue

       
       

    return resultado