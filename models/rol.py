from database import db

class Rol(db.Model):

    __tablename__ = "roles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    descripcion = db.Column(
        db.String(255),
        nullable=False
    )

    usuarios = db.relationship(
        "Usuario",
        backref="rol",
        lazy=True
    )