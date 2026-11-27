from flask import Blueprint, redirect, render_template, request, session, url_for
from db import obtener_datos_dashboard
from models import Estado, Tarea, Tipo, Usuario, db
from utils.decorators import login_required
from utils.helpers import obtener_o_crear_proyecto

tareas_bp = Blueprint("tareas", __name__)


@tareas_bp.route("/main")
@login_required
def main():
    datos = obtener_datos_dashboard()
    return render_template(
        "main.html",
        alias=session.get("alias"),
        img_ruta=session.get("img_ruta"),
        error_add=session.pop("error_add", ""),
        tarea_existe=session.pop("tarea_existe", ""),
        **datos,
    )


@tareas_bp.route("/add", methods=["POST"])
@login_required
def add_tarea():
    tarea_nombre = request.form.get("tarea", "").strip()
    proyecto_nombre = request.form.get("proyecto", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    tipo_nombre = request.form.get("tipo", "").strip()
    estado_nombre = request.form.get("estado", "").strip()
    usuario_raw = request.form.get("usuario", "").strip()

    if not all([tarea_nombre, proyecto_nombre, descripcion, tipo_nombre, estado_nombre, usuario_raw]):
        session["error_add"] = "No puede estar vacío"
        return redirect(url_for("tareas.main"))

    partes_usuario = usuario_raw.split(" ", 1)
    if len(partes_usuario) < 2:
        session["error_add"] = "Formato de usuario inválido (Nombre Apellido)"
        return redirect(url_for("tareas.main"))

    nombre_usuario, apellido_usuario = partes_usuario[0], partes_usuario[1]

    if Tarea.query.filter_by(nombre_tarea=tarea_nombre).first():
        session["tarea_existe"] = "La tarea ya existe"
        return redirect(url_for("tareas.main"))

    tipo_obj = Tipo.query.filter_by(nombre_tipo=tipo_nombre).first()
    estado_obj = Estado.query.filter_by(nombre_estado=estado_nombre).first()
    usuario_obj = Usuario.query.filter_by(
        nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario
    ).first()

    if not (tipo_obj and estado_obj and usuario_obj):
        session["error_add"] = "Tipo, estado o usuario no encontrado en la base de datos"
        return redirect(url_for("tareas.main"))

    try:
        id_proyecto = obtener_o_crear_proyecto(proyecto_nombre)
        nueva_tarea = Tarea(
            nombre_tarea=tarea_nombre,
            descripcion_tarea=descripcion,
            id_proyecto=id_proyecto,
            id_tipo=tipo_obj.id_tipo,
            id_usuario=usuario_obj.id_usuario,
            id_estado=estado_obj.id_estado,
        )
        db.session.add(nueva_tarea)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        session["error_add"] = f"Error en la base de datos: {err}"

    return redirect(url_for("tareas.main"))


@tareas_bp.route("/delete", methods=["POST"])
@login_required
def delete_tarea():
    id_tarea = request.form.get("id_tarea")
    tarea_obj = db.session.get(Tarea, id_tarea)
    if tarea_obj:
        db.session.delete(tarea_obj)
        db.session.commit()
    return redirect(url_for("tareas.main"))


@tareas_bp.route("/main_editar", methods=["GET", "POST"])
@login_required
def main_editar():
    if request.method == "POST":
        id_editar = request.form.get("id_tarea")
        session["id_tarea"] = id_editar
    else:
        id_editar = session.get("id_tarea")

    id_editar = int(id_editar) if id_editar else None
    datos = obtener_datos_dashboard()

    return render_template(
        "main.html",
        alias=session.get("alias"),
        img_ruta=session.get("img_ruta"),
        error_add=session.pop("error_add", ""),
        tarea_existe=session.pop("tarea_existe", ""),
        error_editar=session.pop("error_editar", ""),
        id_editar=id_editar,
        **datos,
    )


@tareas_bp.route("/editar", methods=["POST"])
@login_required
def editar_tarea():
    id_tarea = request.form.get("id_tarea")
    proyecto_nombre = request.form.get("proyecto", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    estado_nombre = request.form.get("estado", "").strip()
    usuario_raw = request.form.get("usuario", "").strip()

    if not all([id_tarea, proyecto_nombre, descripcion, estado_nombre, usuario_raw]):
        session["error_editar"] = "El dato no válido"
        session["id_tarea"] = id_tarea
        return redirect(url_for("tareas.main_editar"))

    partes_usuario = usuario_raw.split(" ", 1)
    if len(partes_usuario) < 2:
        session["error_editar"] = "El dato no válido"
        session["id_tarea"] = id_tarea
        return redirect(url_for("tareas.main_editar"))

    nombre_usuario, apellido_usuario = partes_usuario[0], partes_usuario[1]

    tarea_obj = db.session.get(Tarea, id_tarea)
    estado_obj = Estado.query.filter_by(nombre_estado=estado_nombre).first()
    usuario_obj = Usuario.query.filter_by(
        nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario
    ).first()

    if not (tarea_obj and estado_obj and usuario_obj):
        session["error_editar"] = "Estado o usuario no encontrado"
        session["id_tarea"] = id_tarea
        return redirect(url_for("tareas.main_editar"))

    try:
        tarea_obj.descripcion_tarea = descripcion
        tarea_obj.id_proyecto = obtener_o_crear_proyecto(proyecto_nombre)
        tarea_obj.id_estado = estado_obj.id_estado
        tarea_obj.id_usuario = usuario_obj.id_usuario
        db.session.commit()
    except Exception:
        db.session.rollback()
        session["error_editar"] = "Error al actualizar la tarea"
        session["id_tarea"] = id_tarea
        return redirect(url_for("tareas.main_editar"))

    session.pop("id_tarea", None)
    return redirect(url_for("tareas.main"))
