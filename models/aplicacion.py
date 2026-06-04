from database import db

class Aplicacion(db.Model):

    __tablename__ = "aplicaciones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )