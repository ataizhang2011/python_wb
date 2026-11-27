import html
import re
import bcrypt
from flask import Blueprint, redirect, render_template, request, session, url_for
from db import obtener_datos_dashboard
from models import Usuario, db
from utils.decorators import login_required
from utils.helpers import guardar_avatar

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/main_usuario", methods=["GET", "POST"])
@login_required
def main_usuario():
    if request.method == "GET":
        return redirect(url_for("tareas.main"))

    id_usuario = request.form.get("id_usuario")
    datos = obtener_datos_dashboard(id_usuario=id_usuario)

    return render_template(
        "main.html",
        alias=session.get("alias"),
        img_ruta=session.get("img_ruta"),
        error_add=session.pop("error_add", ""),
        tarea_existe=session.pop("tarea_existe", ""),
        **datos,
    )

@usuario_bp.route("/modificar", methods=["GET", "POST"])
@login_required
def modificar():
    alias = session.get("alias")
    usuario = Usuario.query.filter_by(alias_usuario=alias).first()

    if not usuario:
        return redirect(url_for("auth.index"))

    session["id"] = usuario.id_usuario

    return render_template(
        "modificar.html",
        alias=alias,
        img_ruta=session.get("img_ruta"),
        mensaje=session.pop("mensaje", False),
        nombre_usuario=usuario.nombre_usuario,
        apellido_usuario=usuario.apellido_usuario,
        email_usuario=usuario.email_usuario,
    )

@usuario_bp.route("/update_usuario", methods=["POST"])
@login_required
def update_usuario():
    id_user = session["id"]
    alias_saneado = session["alias"]

    nombre_saneado = html.escape(request.form.get("nombre", "").strip(), quote=True)
    apellido_saneado = html.escape(request.form.get("apellido", "").strip(), quote=True)
    email_saneado = request.form.get("email", "").strip()
    password_saneada = request.form.get("password", "")
    password2_saneada = request.form.get("password2", "")

    if not alias_saneado or not re.match(r"^[^\W\d_]+$", alias_saneado):
        session["mensaje"] = "El alias de usuario no es válido. Solo se permiten letras"
        return redirect(url_for("usuario.modificar"))

    if not password_saneada or not re.match(r"^[= \w]{8,10}$", password_saneada):
        session["mensaje"] = (
            "La contraseña tendrá 8 caracteres como mínimo y 10 como máximo. "
            "Sólo puede contener letras, dígitos, espacios y el símbolo ="
        )
        return redirect(url_for("usuario.modificar"))

    if password_saneada != password2_saneada:
        session["mensaje"] = "Las contraseñas no son iguales"
        return redirect(url_for("usuario.modificar"))

    # Recupera rápidamente el objeto del usuario actual mediante la clave primaria.
    usuario = db.session.get(Usuario, id_user)
    if not usuario:
        return redirect(url_for("auth.index"))

    # Guarda el nuevo avatar y elimina automáticamente el anterior.
    ruta_db, error_img = guardar_avatar(
        request.files.get("imagen"), alias_saneado, session.get("img_ruta")
    )
    if error_img:
        session["mensaje"] = error_img
        return redirect(url_for("usuario.modificar"))

    password_encriptada = bcrypt.hashpw(
        password_saneada.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    try:
        # Modifica directamente las propiedades del objeto; al confirmar la transacción, se ejecuta automáticamente una operación `UPDATE`.
        usuario.nombre_usuario = nombre_saneado
        usuario.apellido_usuario = apellido_saneado
        usuario.email_usuario = email_saneado
        usuario.password_user = password_encriptada
        usuario.img_ruta = ruta_db

        db.session.commit()
        session["img_ruta"] = ruta_db
    except Exception as err:
        db.session.rollback()
        session["mensaje"] = f"Error en la base de datos: {err}"
        return redirect(url_for("usuario.modificar"))

    return redirect(url_for("tareas.main"))
