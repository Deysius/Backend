from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

from database import db
from extensions import bcrypt

from models.meta import Meta
from models.rol import Rol
from models.usuario import Usuario
from models.rol_aplicacion import RolAplicacion
from models.proyecto import Proyecto
from models.avance_proyecto import AvanceProyecto
from models.registro_actividad import RegistroActividad
from models.plan_mejora import PlanMejora
from models.aplicacion import Aplicacion

from routes.metas import metas_bp
from routes.proyectos import proyectos_bp
from routes.avances import avances_bp
from routes.roles import roles_bp
from routes.usuarios import usuarios_bp
from routes.rol_aplicacion import rol_aplicacion_bp
from routes.registro_actividad import actividad_bp
from routes.historico import historico_bp
from routes.aplicaciones import aplicaciones_bp

from services.analisis_proyectos import analisis_proyectos_bp
from services.productividad import productividad_bp
from services.comparacion import comparacion_bp
from services.proyectos_analisis import analisis_proyecto_bp
from services.uso_aplicaciones import uso_bp
from services.ranking import ranking_bp
from services.promedio_semestral import promedio_bp
from services.evaluacion_global import evaluacion_bp
from services.plan_mejora import plan_bp

app = Flask(__name__)

# JWT
app.config["JWT_SECRET_KEY"] = "clave_super_secreta_123"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

jwt = JWTManager(app)

# CORS
CORS(app)

# Bcrypt
bcrypt.init_app(app)

# Base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///timewise.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Blueprints
app.register_blueprint(aplicaciones_bp)
app.register_blueprint(metas_bp)
app.register_blueprint(proyectos_bp)
app.register_blueprint(avances_bp)
app.register_blueprint(analisis_proyectos_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(rol_aplicacion_bp)
app.register_blueprint(actividad_bp)
app.register_blueprint(productividad_bp)
app.register_blueprint(historico_bp)
app.register_blueprint(comparacion_bp)
app.register_blueprint(plan_bp)
app.register_blueprint(analisis_proyecto_bp)
app.register_blueprint(uso_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(promedio_bp)
app.register_blueprint(evaluacion_bp)

# Crear tablas y datos iniciales
with app.app_context():

    db.create_all()

    # Rol Administrador
    admin_rol = Rol.query.filter_by(
        nombre="Administrador"
    ).first()

    if not admin_rol:

        admin_rol = Rol(
            nombre="Administrador",
            descripcion="Administrador del sistema"
        )

        db.session.add(admin_rol)
        db.session.commit()

    # Rol Empleado
    empleado_rol = Rol.query.filter_by(
        nombre="Empleado"
    ).first()

    if not empleado_rol:

        empleado_rol = Rol(
            nombre="Empleado",
            descripcion="Usuario estándar"
        )

        db.session.add(empleado_rol)
        db.session.commit()

    # Usuario Administrador
    admin = Usuario.query.filter_by(
        correo="admin@timewise.com"
    ).first()

    if not admin:

        password_hash = bcrypt.generate_password_hash(
            "admin123"
        ).decode("utf-8")

        admin = Usuario(
            nombre="Administrador",
            correo="admin@timewise.com",
            password_hash=password_hash,
            rol_id=admin_rol.id
        )

        db.session.add(admin)
        db.session.commit()

        print("Administrador creado correctamente")
@app.route("/")
def home():
    return {
        "message": "Backend funcionando"
    }


if __name__ == "__main__":
    app.run(debug=True)
    
@app.route("/crear-admin")
def crear_admin():

    admin = Usuario.query.filter_by(
        correo="admin@timewise.com"
    ).first()

    if admin:
        return {
            "mensaje": "El administrador ya existe"
        }

    admin_rol = Rol.query.filter_by(
        nombre="Administrador"
    ).first()

    password_hash = bcrypt.generate_password_hash(
        "admin123"
    ).decode("utf-8")

    admin = Usuario(
        nombre="Administrador",
        correo="admin@timewise.com",
        password_hash=password_hash,
        rol_id=admin_rol.id
    )

    db.session.add(admin)
    db.session.commit()

    return {
        "mensaje": "Administrador creado"
    }