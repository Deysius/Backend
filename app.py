from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from database import db

from models.meta import Meta
from routes.metas import metas_bp
from models.rol import Rol
from models.usuario import Usuario
from models.rol_aplicacion import RolAplicacion
from models.proyecto import Proyecto
from models.avance_proyecto import AvanceProyecto
from routes.proyectos import proyectos_bp
from routes.avances import avances_bp
from services.analisis_proyectos import analisis_proyectos_bp
from routes.roles import roles_bp
from routes.usuarios import usuarios_bp
from routes.rol_aplicacion import rol_aplicacion_bp
from models.registro_actividad import RegistroActividad
from routes.registro_actividad import actividad_bp
from services.productividad import productividad_bp
from routes.historico import historico_bp
from services.comparacion import comparacion_bp
from models.plan_mejora import PlanMejora
from services.proyectos_analisis import analisis_proyecto_bp
from services.uso_aplicaciones import uso_bp
from services.ranking import ranking_bp
from flask_jwt_extended import JWTManager
from models.aplicacion import Aplicacion
from routes.aplicaciones import aplicaciones_bp
from services.promedio_semestral import (
    promedio_bp
)
from services.evaluacion_global import (
    evaluacion_bp
)
from services.plan_mejora import plan_bp
app = Flask(__name__)
from extensions import bcrypt

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "clave_super_secreta_123"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
from datetime import timedelta

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
jwt = JWTManager(app)

bcrypt.init_app(app)
CORS(app)


app.register_blueprint(
    aplicaciones_bp
)
app.register_blueprint(metas_bp)
app.register_blueprint(proyectos_bp)
app.register_blueprint(avances_bp)
app.register_blueprint(
    analisis_proyectos_bp
)
app.register_blueprint(roles_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(
    rol_aplicacion_bp
)
app.register_blueprint(
    actividad_bp
)
app.register_blueprint(
    productividad_bp
)
app.register_blueprint(
    historico_bp
)
app.register_blueprint(
    comparacion_bp
)
app.register_blueprint(
    plan_bp
)
app.register_blueprint(
    analisis_proyecto_bp
)
app.register_blueprint(
    uso_bp
)
app.register_blueprint(
    ranking_bp
)
app.register_blueprint(
    promedio_bp
)
app.register_blueprint(
    evaluacion_bp
)

# CONFIGURACIÓN BASE DE DATOS
import os

# Render inyectará automáticamente una variable llamada DATABASE_URL
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///timewise.db')

# Si la URL viene de Render (Postgres), a veces empieza por 'postgres://', 
# pero SQLAlchemy requiere 'postgresql://'.
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


# INICIALIZAR DB

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"message": "Backend funcionando"}

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
    
