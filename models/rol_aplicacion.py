from database import db

class RolAplicacion(db.Model):

    __tablename__ = "rol_aplicacion"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    rol_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )

    aplicacion_id = db.Column(
        db.Integer,
        db.ForeignKey("aplicaciones.id"),
        nullable=False
    )

    es_productiva = db.Column(
        db.Boolean,
        nullable=False
    )
    rol = db.relationship(
    "Rol",
    backref="aplicaciones_productivas"
)