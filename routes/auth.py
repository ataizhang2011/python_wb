import html
import re
import bcrypt
from flask import Blueprint, redirect, render_template, request, session, url_for
from models import Usuario, db
from utils.helpers import guardar_avatar

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    error_login = session.pop("error_login", False)
    return render_template("index.html", error_login=error_login)

@auth_bp.route("/login", methods=["POST"])
def login():
    user_raw = request.form.get("user", "").strip().lower()
    user_saneado = html.escape(user_raw, quote=True)
    pass_saneada = request.form.get("pass", "")

    if not user_saneado or not re.match(r"^[^\W\d_]+$", user_saneado):
        session["error_login"] = "El alias de usuario no es válido. Solo se permiten letras"
        return redirect(url_for("auth.index"))

    if not pass_saneada or not re.match(r"^[= \w]+$", pass_saneada):
        session["error_login"] = "Formato de contraseña no válido (solo letras, números, espacios y =)"
        return redirect(url_for("auth.index"))

    # ORM Consultar usuario
    usuario = Usuario.query.filter_by(alias_usuario=user_saneado).first()

    if not usuario:
        session["error_login"] = "El usuario no existe en la base de datos"
        return redirect(url_for("auth.index"))

    password_BD = usuario.password_user
    if password_BD.startswith("$2y$"):
        password_BD = "$2b$" + password_BD[4:]

    try:
        ok_password = bcrypt.checkpw(pass_saneada.encode("utf-8"), password_BD.encode("utf-8"))
    except Exception:
        ok_password = False

    if not ok_password:
        session["error_login"] = "Error en el usuario o la contraseña"
        return redirect(url_for("auth.index"))

    session["id"] = usuario.id_usuario
    session["alias"] = request.form.get("user")
    session["img_ruta"] = usuario.img_ruta

    return redirect(url_for("tareas.main"))

@auth_bp.route("/registro")
def registro():
    error_registro = session.pop("error_registro", False)
    return render_template("registro.html", error_registro=error_registro)

@auth_bp.route("/registado", methods=["POST"])
def registado():
    nombre_saneado = html.escape(request.form.get("nombre", "").strip(), quote=True)
    apellido_saneado = html.escape(request.form.get("apellido", "").strip(), quote=True)
    email_saneado = request.form.get("email", "").strip()
    alias_saneado = html.escape(request.form.get("alias", "").strip().lower(), quote=True)
    password_saneada = request.form.get("password", "")
    password2_saneada = request.form.get("password2", "")

    if not alias_saneado or not re.match(r"^[^\W\d_]+$", alias_saneado):
        session["error_registro"] = "El alias de usuario no es válido. Solo se permiten letras"
        return redirect(url_for("auth.registro"))

    if not password_saneada or not re.match(r"^[= \w]{8,10}$", password_saneada):
        session["error_registro"] = (
            "La contraseña tendrá 8 caracteres como mínimo y 10 como máximo. "
            "Sólo puede contener letras, dígitos, espacios y el símbolo ="
        )
        return redirect(url_for("auth.registro"))

    if password_saneada != password2_saneada:
        session["error_registro"] = "Las contraseñas no son iguales"
        return redirect(url_for("auth.registro"))

    # Comprueba si el nombre de usuario ya existe
    if Usuario.query.filter_by(alias_usuario=alias_saneado).first():
        session["error_registro"] = "El alias de usuario ya existe"
        return redirect(url_for("auth.registro"))

    # Validar y guardar avatar
    ruta_db, error_img = guardar_avatar(request.files.get("imagen"), alias_saneado)
    if error_img:
        session["error_registro"] = error_img
        return redirect(url_for("auth.registro"))

    password_encriptada = bcrypt.hashpw(
        password_saneada.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    try:
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_saneado,
            apellido_usuario=apellido_saneado,
            email_usuario=email_saneado,
            alias_usuario=alias_saneado,
            password_user=password_encriptada,
            img_ruta=ruta_db,
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        session["error_registro"] = f"Error al registrar usuario: {err}"
        return redirect(url_for("auth.registro"))

    return redirect(url_for("auth.index"))

@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.index"))
