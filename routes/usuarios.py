from flask import Blueprint, request

from database import db

from models.usuario import Usuario
from models.rol import Rol
from models.proyecto import Proyecto
from models.avance_proyecto import AvanceProyecto 
from models.registro_actividad import RegistroActividad
from models.historico_productividad import HistoricoProductividad
from extensions import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

usuarios_bp = Blueprint(
    "usuarios",
    __name__
)

def es_admin():
    claims = get_jwt()
    return claims.get("rol") == "Administrador"


@usuarios_bp.route(
    "/usuarios",
    methods=["GET"]
)
@jwt_required()
def obtener_usuarios():
    usuarios = Usuario.query.all()
    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol_id": usuario.rol_id,
            "rol": usuario.rol.nombre if usuario.rol else None
        })

    return resultado, 200


@usuarios_bp.route(
    "/usuarios",
    methods=["POST"]
)
@jwt_required()
def crear_usuario():
    data = request.json
   
    if not es_admin():
        return {
            "error": "Acceso denegado"
        }, 403
    
    if not data:
        return {
            "error": "Datos requeridos"
        }, 400

    if not data.get("nombre", "").strip():
        return {
            "error": "Nombre requerido"
        }, 400

    if not data.get("correo"):
        return {
            "error": "Correo requerido"
        }, 400

    if "@" not in data["correo"]:
        return {
            "error": "Correo inválido"
        }, 400

    if not data.get("password"):
        return {
            "error": "Contraseña requerida"
        }, 400

    if len(data["password"]) < 8:
        return {
            "error": "La contraseña debe tener mínimo 8 caracteres"
        }, 400

    if not data.get("rol_id"):
        return {
            "error": "Rol requerido"
        }, 400

    rol = Rol.query.get(data["rol_id"])

    if not rol:
        return {
            "error": "El rol seleccionado no existe"
        }, 400

    usuario_existente = Usuario.query.filter_by(
        correo=data["correo"]
    ).first()

    if usuario_existente:
        return {
            "error": "El correo ya existe"
        }, 400

    password_hash = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    usuario = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        password_hash=password_hash,
        rol_id=data["rol_id"]
    )

    db.session.add(usuario)
    db.session.commit()

    return {
        "mensaje": "Usuario creado",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": rol.nombre
        }
    }, 201


@usuarios_bp.route(
    "/login",
    methods=["POST"]
)
def login():
    data = request.json

    if not data:
        return {
            "error": "Datos requeridos"
        }, 400

    if not data.get("correo"):
        return {
            "error": "Correo requerido"
        }, 400

    if not data.get("password"):
        return {
            "error": "Contraseña requerida"
        }, 400

    usuario = Usuario.query.filter_by(
        correo=data["correo"]
    ).first()

    if not usuario:
        return {
            "error": "Credenciales incorrectas"
        }, 401

    if not bcrypt.check_password_hash(
        usuario.password_hash,
        data["password"]
    ):
        return {
            "error": "Credenciales incorrectas"
        }, 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            "rol": usuario.rol.nombre if usuario.rol else None
        }
    )

    return {
        "mensaje": "Login exitoso",
        "token": token,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol_id": usuario.rol_id,
            "rol": usuario.rol.nombre
        }
    }, 200


@usuarios_bp.route(
    "/perfil",
    methods=["GET"]
)
@jwt_required()
def perfil():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(int(usuario_id))

    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }, 404

    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "rol": usuario.rol.nombre if usuario.rol else None
    }, 200    
    

@usuarios_bp.route(
    "/usuarios/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def actualizar_usuario(id):
    usuario = Usuario.query.get(id)
    
    if not es_admin():
        return {
            "error": "Acceso denegado"
        }, 403

    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }, 404

    data = request.json

    if "nombre" in data:
        usuario.nombre = data["nombre"]

    if "correo" in data:
        usuario.correo = data["correo"]

    if "rol_id" in data:
        rol = Rol.query.get(data["rol_id"])
        if not rol:
            return {
                "error": "Rol no existe"
            }, 400
        usuario.rol_id = data["rol_id"]

    db.session.commit()

    return {
        "mensaje": "Usuario actualizado"
    }, 200

try:
    from models.plan_mejora import PlanMejora
except ImportError:
    
    from models.planes_mejora import PlanMejora 



@usuarios_bp.route(
    "/usuarios/<int:id>", 
    methods=["DELETE"]
)
@jwt_required()
def eliminar_usuario(id):
    if not es_admin():
        return {
            "error": "Acceso denegado"
        }, 403

    usuario = Usuario.query.get(id)
    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }, 404

    try:
        
        PlanMejora.query.filter_by(usuario_id=id).delete()

   
        HistoricoProductividad.query.filter_by(usuario_id=id).delete()

   
        RegistroActividad.query.filter_by(usuario_id=id).delete()

        proyectos_usuario = Proyecto.query.filter_by(usuario_id=id).all()
        for proyecto in proyectos_usuario:
            AvanceProyecto.query.filter_by(proyecto_id=proyecto.id).delete()

        Proyecto.query.filter_by(usuario_id=id).delete()

        
        db.session.delete(usuario)
        db.session.commit()

        return {
            "mensaje": "Usuario y todo su historial eliminados con éxito"
        }, 200

    except Exception as e:
        db.session.rollback()
        return {
            "error": f"Error en la base de datos: {str(e)}"
        }, 500
   
    

@usuarios_bp.route(
    "/debug-token",
    methods=["GET"] 
)
@jwt_required()
def debug_token():
    return get_jwt(), 200