from database import db

class HistoricoProductividad(db.Model):

    __tablename__ = "historico_productividad"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    periodo = db.Column(
        db.String(50),
        nullable=False
    )

    indice_productividad = db.Column(
        db.Float,
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )