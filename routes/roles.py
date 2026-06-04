from flask import Blueprint, request

from database import db
from models.rol import Rol

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

roles_bp = Blueprint(
    "roles",
    __name__
)

def es_admin():

    claims = get_jwt()

    return claims.get("rol") == "Administrador"


@roles_bp.route(
    "/roles",
    methods=["GET"]
)
@jwt_required()
def obtener_roles():

    roles = Rol.query.all()

    resultado = []

    for rol in roles:
        resultado.append({
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion
        })

    return resultado

@roles_bp.route(
    "/roles",
    methods=["POST"]
)
@jwt_required()
def crear_rol():
    print("USUARIO:", get_jwt_identity())
    

    if not es_admin():  
        return {
            "error": "Acceso denegado"
        }, 403

    data = request.json

    if not data["nombre"].strip():
        return {
            "error": "Nombre requerido"
        }, 400

    rol = Rol(
        nombre=data["nombre"],
        descripcion=data["descripcion"]
    )

    db.session.add(rol)
    db.session.commit()

    return {
        "mensaje": "Rol creado"
    }

@roles_bp.route(
    "/roles/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def actualizar_rol(id):
    if not es_admin():
        return {
            "error": "Acceso denegado"
        }, 403

    rol = Rol.query.get(id)

    if not rol:

        return {
            "error": "Rol no encontrado"
        }, 404

    data = request.json

    rol.nombre = data["nombre"]

    rol.descripcion = data["descripcion"]

    db.session.commit()

    return {
        "mensaje": "Rol actualizado"
    }, 200
    
    
@roles_bp.route(
    "/roles/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def eliminar_rol(id):
    if not es_admin():
        return {
            "error": "Acceso denegado"
        }, 403

    rol = Rol.query.get(id)

    if not rol:

        return {
            "error": "Rol no encontrado"
        }, 404

    db.session.delete(rol)

    db.session.commit()

    return {
        "mensaje": "Rol eliminado"
    }, 200
    
    
@roles_bp.route("/test-token")
@jwt_required()
def test_token():
    return {
        "usuario": get_jwt_identity()
    }, 200