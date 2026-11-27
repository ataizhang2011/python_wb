from functools import wraps
import bcrypt
from flask import Blueprint, jsonify, request, session
from sqlalchemy.orm import joinedload
from models import Estado, Tarea, Tipo, Usuario, db
from utils.helpers import obtener_o_crear_proyecto

api_bp = Blueprint("api", __name__, url_prefix="/api")


# 1. Decorador de autenticación diseñado específicamente para APIs (devuelve una respuesta JSON 401 cuando no se ha iniciado sesión, en lugar de redirigir a una página HTML)
def api_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "alias" not in session:
            return jsonify({"status": "error", "message": "No autorizado. Inicia sesión primero."}), 401
        return f(*args, **kwargs)
    return decorated


# 2. Función auxiliar de serialización: convierte objetos ORM de tipo Tarea en diccionarios.
def tarea_to_dict(t):
    return {
        "id_tarea": t.id_tarea,
        "nombre_tarea": t.nombre_tarea,
        "descripcion_tarea": t.descripcion_tarea,
        "proyecto": t.nombre_proyecto,
        "tipo": t.nombre_tipo,
        "estado": t.nombre_estado,
        "assigned_to": t.assigned_to,
        "id_usuario": t.id_usuario,
        "fecha_ini": t.fecha_ini.isoformat() if t.fecha_ini else None,
        "fecha_actua": t.fecha_actua.isoformat() if t.fecha_actua else None,
    }


# ==========================================
# API de autenticación (Auth)
# ==========================================
@api_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    alias = data.get("user", "").strip().lower()
    password = data.get("pass", "")

    if not alias or not password:
        return jsonify({"status": "error", "message": "Usuario y contraseña requeridos"}), 400

    usuario = Usuario.query.filter_by(alias_usuario=alias).first()
    if not usuario:
        return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

    password_BD = usuario.password_user
    if password_BD.startswith("$2y$"):
        password_BD = "$2b$" + password_BD[4:]

    try:
        ok = bcrypt.checkpw(password.encode("utf-8"), password_BD.encode("utf-8"))
    except Exception:
        ok = False

    if not ok:
        return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

    session["id"] = usuario.id_usuario
    session["alias"] = usuario.alias_usuario
    session["img_ruta"] = usuario.img_ruta

    return jsonify({
        "status": "success",
        "message": "Login exitoso",
        "data": {
            "id_usuario": usuario.id_usuario,
            "alias": usuario.alias_usuario,
            "nombre_completo": usuario.usuario,
            "img_ruta": usuario.img_ruta,
        }
    }), 200


# ==========================================
# API de recursos de tareas (CRUD para tareas)
# ==========================================

# [GET] Obtener lista de tareas (admite filtrado mediante ?id_usuario=1)
@api_bp.route("/tareas", methods=["GET"])
@api_login_required
def get_tareas():
    id_usuario = request.args.get("id_usuario", type=int)

    query = Tarea.query.options(
        joinedload(Tarea.proyecto),
        joinedload(Tarea.tipo),
        joinedload(Tarea.usuario),
        joinedload(Tarea.estado),
    )

    if id_usuario:
        query = query.filter(Tarea.id_usuario == id_usuario)

    tareas = query.all()
    return jsonify({
        "status": "success",
        "total": len(tareas),
        "data": [tarea_to_dict(t) for t in tareas]
    }), 200


# [GET] Obtener los detalles de una tarea específica
@api_bp.route("/tareas/<int:id_tarea>", methods=["GET"])
@api_login_required
def get_tarea_detalle(id_tarea):
    tarea = db.session.get(Tarea, id_tarea)
    if not tarea:
        return jsonify({"status": "error", "message": "Tarea no encontrada"}), 404

    return jsonify({
        "status": "success",
        "data": tarea_to_dict(tarea)
    }), 200


# [POST] Crear una nueva tarea
@api_bp.route("/tareas", methods=["POST"])
@api_login_required
def create_tarea():
    data = request.get_json(silent=True) or {}

    nombre_tarea = data.get("tarea", "").strip()
    proyecto_nombre = data.get("proyecto", "").strip()
    descripcion = data.get("descripcion", "").strip()
    tipo_nombre = data.get("tipo", "").strip()
    estado_nombre = data.get("estado", "").strip()
    id_usuario = data.get("id_usuario")

    if not all([nombre_tarea, proyecto_nombre, descripcion, tipo_nombre, estado_nombre, id_usuario]):
        return jsonify({"status": "error", "message": "Faltan campos obligatorios"}), 400

    if Tarea.query.filter_by(nombre_tarea=nombre_tarea).first():
        return jsonify({"status": "error", "message": "La tarea ya existe"}), 409

    tipo_obj = Tipo.query.filter_by(nombre_tipo=tipo_nombre).first()
    estado_obj = Estado.query.filter_by(nombre_estado=estado_nombre).first()
    usuario_obj = db.session.get(Usuario, id_usuario)

    if not (tipo_obj and estado_obj and usuario_obj):
        return jsonify({"status": "error", "message": "Tipo, estado o usuario inválido"}), 400

    try:
        id_proyecto = obtener_o_crear_proyecto(proyecto_nombre)
        nueva_tarea = Tarea(
            nombre_tarea=nombre_tarea,
            descripcion_tarea=descripcion,
            id_proyecto=id_proyecto,
            id_tipo=tipo_obj.id_tipo,
            id_usuario=usuario_obj.id_usuario,
            id_estado=estado_obj.id_estado,
        )
        db.session.add(nueva_tarea)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Tarea creada correctamente",
            "data": tarea_to_dict(nueva_tarea)
        }), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(err)}), 500


# [PUT] Actualizar una tarea específica
@api_bp.route("/tareas/<int:id_tarea>", methods=["PUT"])
@api_login_required
def update_tarea(id_tarea):
    tarea = db.session.get(Tarea, id_tarea)
    if not tarea:
        return jsonify({"status": "error", "message": "Tarea no encontrada"}), 404

    data = request.get_json(silent=True) or {}

    if "descripcion" in data:
        tarea.descripcion_tarea = data["descripcion"].strip()

    if "proyecto" in data and data["proyecto"].strip():
        tarea.id_proyecto = obtener_o_crear_proyecto(data["proyecto"].strip())

    if "estado" in data:
        estado_obj = Estado.query.filter_by(nombre_estado=data["estado"].strip()).first()
        if not estado_obj:
            return jsonify({"status": "error", "message": "Estado no válido"}), 400
        tarea.id_estado = estado_obj.id_estado

    if "id_usuario" in data:
        usuario_obj = db.session.get(Usuario, data["id_usuario"])
        if not usuario_obj:
            return jsonify({"status": "error", "message": "Usuario no válido"}), 400
        tarea.id_usuario = usuario_obj.id_usuario

    try:
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Tarea actualizada",
            "data": tarea_to_dict(tarea)
        }), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(err)}), 500


# [ELIMINAR] Eliminar la tarea especificada
@api_bp.route("/tareas/<int:id_tarea>", methods=["DELETE"])
@api_login_required
def delete_tarea(id_tarea):
    tarea = db.session.get(Tarea, id_tarea)
    if not tarea:
        return jsonify({"status": "error", "message": "Tarea no encontrada"}), 404

    try:
        db.session.delete(tarea)
        db.session.commit()
        return jsonify({"status": "success", "message": "Tarea eliminada"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(err)}), 500


# ==========================================
# API de lista de usuarios (Usuarios)
# ==========================================
@api_bp.route("/usuarios", methods=["GET"])
@api_login_required
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify({
        "status": "success",
        "data": [
            {
                "id_usuario": u.id_usuario,
                "alias": u.alias_usuario,
                "nombre_completo": u.usuario,
                "email": u.email_usuario,
                "img_ruta": u.img_ruta,
            }
            for u in usuarios
        ]
    }), 200
