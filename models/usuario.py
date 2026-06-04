from database import db

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    correo = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    rol_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )

    proyectos = db.relationship(
        "Proyecto",
        backref="usuario",
        lazy=True
    )

    actividades = db.relationship(
        "RegistroActividad",
        backref="usuario",
        lazy=True
    )

    planes = db.relationship(
        "PlanMejora",
        backref="usuario_plan",
        lazy=True
    )