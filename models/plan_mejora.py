from database import db

class PlanMejora(db.Model):

    __tablename__ = "planes_mejora"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recomendacion = db.Column(
        db.String(300),
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )