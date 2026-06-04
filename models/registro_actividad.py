from database import db

class RegistroActividad(db.Model):

    __tablename__ = "registro_actividad"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    tiempo_activo = db.Column(
        db.Float,
        nullable=False
    )

    tiempo_inactivo = db.Column(
        db.Float,
        nullable=False
    )

    clicks_mouse = db.Column(
        db.Integer,
        nullable=False
    )

    teclas_presionadas = db.Column(
        db.Integer,
        nullable=False
    )

    movimiento_mouse = db.Column(
        db.Float,
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    aplicacion_id = db.Column(
        db.Integer,
        db.ForeignKey("aplicaciones.id"),
        nullable=False
    )