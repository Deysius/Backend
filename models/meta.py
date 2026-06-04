from database import db

class Meta(db.Model):

    __tablename__ = "metas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(200),
        nullable=False
    )

    objetivo = db.Column(
        db.Float,
        nullable=False
    )

    progreso = db.Column(
        db.Float,
        default=0
    )

    prioridad = db.Column(
        db.String(50),
        nullable=False
    )
    usuario_id = db.Column(
    db.Integer,
    db.ForeignKey("usuarios.id"),
    nullable=False
)