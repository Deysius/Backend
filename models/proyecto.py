from database import db

class Proyecto(db.Model):

    __tablename__ = "proyectos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    descripcion = db.Column(
        db.String(500),
        nullable=False
    )

    fecha_inicio = db.Column(
        db.Date,
        nullable=False
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=False
    )

    horas_estimadas = db.Column(
        db.Float,
        nullable=False
    )

    prioridad = db.Column(
        db.String(50),
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

    avances = db.relationship(
        "AvanceProyecto",
        backref="proyecto",
        lazy=True
    )