from database import db

class AvanceProyecto(db.Model):

    __tablename__ = "avances_proyecto"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    horas_trabajadas = db.Column(
        db.Float,
        nullable=False
    )

    descripcion = db.Column(
        db.String(500),
        nullable=False
    )

    proyecto_id = db.Column(
        db.Integer,
        db.ForeignKey("proyectos.id"),
        nullable=False
    )