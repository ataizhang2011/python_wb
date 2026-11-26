import html
import re
import bcrypt
import os, uuid
from db import get_db_connection, obtener_datos_dashboard
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

app.secret_key = "working_better_secret_key_change_me"

@app.route("/")
def index():
    error_login = session.pop("error_login", False)
    return render_template("index.html", error_login=error_login)

@app.route("/login", methods=["POST"])
def login():
    user_raw = request.form.get("user", "").strip().lower()
    user_saneado = html.escape(user_raw, quote=True)
    pass_saneada = request.form.get("pass", "")

    patron_alias = r"^[^\W\d_]+$"
    patron_pass = r"^[= \w]+$"

    if not user_saneado or not re.match(patron_alias, user_saneado):
        session["error_login"] = (
            "El alias de usuario no es válido. Solo se permiten letras"
        )
        return redirect(url_for("index"))

    if not pass_saneada or not re.match(patron_pass, pass_saneada):
        session["error_login"] = (
            "Formato de contraseña no válido (solo letras, números, espacios y =)"
        )
        return redirect(url_for("index"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id_usuario, password_user, img_ruta FROM usuarios WHERE alias_usuario = %s"
            cursor.execute(sql, (user_saneado,))
            resultado_user = cursor.fetchone()
    finally:
        conn.close()

    if not resultado_user:
        session["error_login"] = "El usuario no existe en la base de datos"
        return redirect(url_for("index"))

    password_BD = resultado_user["password_user"]

    if password_BD.startswith("$2y$"):
        password_BD = "$2b$" + password_BD[4:]

    try:
        ok_password = bcrypt.checkpw(
            pass_saneada.encode("utf-8"), password_BD.encode("utf-8")
        )
    except Exception as e:
        print(f"Bcrypt Excepción de validación: {e} | El valor de la contraseña en la base de datos es: {password_BD}")
        ok_password = False

    if not ok_password:
        session["error_login"] = "Error en el usuario o la contraseña"
        return redirect(url_for("index"))

    session["id"] = resultado_user["id_usuario"]
    session["alias"] = request.form.get("user")
    session["img_ruta"] = resultado_user["img_ruta"]

    return redirect(url_for("main"))


@app.route("/main")
def main():
    if "alias" not in session:
        return redirect(url_for("index"))
    
    alias = session.get("alias")
    img_ruta = session.get("img_ruta")
    error_add = session.pop("error_add", "")
    tarea_existe = session.pop("tarea_existe", "")

    datos = obtener_datos_dashboard()

    return render_template(
        "main.html",
        alias=alias,
        img_ruta=img_ruta,
        error_add=error_add,
        tarea_existe=tarea_existe,
        **datos,
    )

@app.route("/add", methods=["POST"])
def add_tarea():
    if "alias" not in session:
        return redirect(url_for("index"))
    
    tarea = request.form.get("tarea", "").strip()
    proyecto = request.form.get("proyecto", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    tipo = request.form.get("tipo", "").strip()
    estado = request.form.get("estado", "").strip()
    usuario_raw = request.form.get("usuario", "").strip()

    if not all([tarea, proyecto, descripcion, tipo, estado, usuario_raw]):
        session["error_add"] = "No puede estar vacío"
        return redirect(url_for("main"))
    
    partes_usuario = usuario_raw.split(" ", 1)
    if len(partes_usuario) < 2:
        session["error_add"] = "Formato de usuario inválido (Nombre Apellido)"
        return redirect(url_for("main"))

    nombre_usuario, apellido_usuario = partes_usuario[0], partes_usuario[1]

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT nombre_tarea FROM tareas WHERE nombre_tarea = %s",
                (tarea,),
            ) 
            if cursor.fetchone():
                session["tarea_existe"] = "La tarea ya existe"
                return redirect(url_for("main"))
            
            cursor.execute(
                "SELECT id_proyecto FROM proyectos WHERE nombre_proyecto = %s",
                (proyecto,),
            )
            pro_row = cursor.fetchone()

            if pro_row:
                id_proyecto = pro_row["id_proyecto"]
            else:
                cursor.execute(
                    "INSERT INTO proyectos (nombre_proyecto) VALUES (%s)",
                    (proyecto,),
                )
                id_proyecto = cursor.lastrowid
            
            cursor.execute(
                "SELECT id_tipo FROM tipos WHERE nombre_tipo = %s", (tipo,)
            )
            tipo_row = cursor.fetchone()    

            cursor.execute(
                "SELECT id_estado FROM estados WHERE nombre_estado = %s",
                (estado,),
            )
            estado_row = cursor.fetchone()

            cursor.execute(
                "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND apellido_usuario = %s",
                (nombre_usuario, apellido_usuario),
            )
            usuario_row = cursor.fetchone()

            if not (tipo_row and estado_row and usuario_row):
                session["error_add"] = (
                    "Tipo, estado o usuario no encontrado en la base de datos"
                )
                return redirect(url_for("main"))
            
            sql_insert = """
                INSERT INTO tareas (nombre_tarea, descripcion_tarea, id_proyecto, id_tipo, id_usuario, id_estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql_insert,
                (
                    tarea,
                    descripcion,
                    id_proyecto,
                    tipo_row["id_tipo"],
                    usuario_row["id_usuario"],
                    estado_row["id_estado"],
                ),
            )
        conn.commit()

    except Exception as err:
        conn.rollback()
        print(f"Error al añadir tarea: {err}")
        session["error_add"] = f"Error en la base de datos: {err}"
    finally:
        conn.close()   
    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_tarea():
    if "alias" not in session:
        return redirect(url_for("index"))
    
    id_tarea = request.form.get("id_tarea")

    if id_tarea:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM tareas WHERE id_tarea = %s", (id_tarea,)
                )
            conn.commit()
        finally:
            conn.close()
    return redirect(url_for("main"))

@app.route("/main_editar", methods=["GET", "POST"])
def main_editar():
    if "alias" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        id_editar = request.form.get("id_tarea")
        session["id_tarea"] = id_editar
    else:
        id_editar = session.get("id_tarea")

    id_editar = int(id_editar) if id_editar else None

    alias = session.get("alias")
    img_ruta = session.get("img_ruta")
    error_add = session.pop("error_add", "")
    tarea_existe = session.pop("tarea_existe", "")
    error_editar = session.pop("error_editar", "")

    datos = obtener_datos_dashboard()

    return render_template(
        "main.html",
        alias=alias,
        img_ruta=img_ruta,
        error_add=error_add,
        tarea_existe=tarea_existe,
        error_editar=error_editar,
        id_editar=id_editar,
        **datos,
    )

@app.route("/editar", methods=["POST"])
def editar_tarea():
    if "alias" not in session:
        return redirect(url_for("index"))

    id_tarea = request.form.get("id_tarea")
    proyecto = request.form.get("proyecto", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    estado = request.form.get("estado", "").strip()
    usuario_raw = request.form.get("usuario", "").strip()

    if not all([id_tarea, proyecto, descripcion, estado, usuario_raw]):
        session["error_editar"] = "El dato no válido"
        session["id_tarea"] = id_tarea
        return redirect(url_for("main_editar"))

    partes_usuario = usuario_raw.split(" ", 1)
    if len(partes_usuario) < 2:
        session["error_editar"] = "El dato no válido"
        session["id_tarea"] = id_tarea
        return redirect(url_for("main_editar"))

    nombre_usuario, apellido_usuario = partes_usuario[0], partes_usuario[1]

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_proyecto FROM proyectos WHERE nombre_proyecto = %s",
                (proyecto,),
            )
            id_pro = cursor.fetchone()

            if id_pro:
                id_proyecto = id_pro["id_proyecto"]
            else:
                cursor.execute(
                    "INSERT INTO proyectos (nombre_proyecto) VALUES (%s)",
                    (proyecto,),
                )
                id_proyecto = (
                    cursor.lastrowid
                )

            cursor.execute(
                "SELECT id_estado FROM estados WHERE nombre_estado = %s",
                (estado,),
            )
            id_est = cursor.fetchone()

            cursor.execute(
                "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND apellido_usuario = %s",
                (nombre_usuario, apellido_usuario),
            )
            id_usua = cursor.fetchone()

            if not (id_est and id_usua):
                session["error_editar"] = "Estado o usuario no encontrado"
                session["id_tarea"] = id_tarea
                return redirect(url_for("main_editar"))

            sql_update = """
                UPDATE tareas 
                SET descripcion_tarea = %s, id_proyecto = %s, id_estado = %s, id_usuario = %s 
                WHERE id_tarea = %s
            """
            cursor.execute(
                sql_update,
                (
                    descripcion,
                    id_proyecto,
                    id_est["id_estado"],
                    id_usua["id_usuario"],
                    id_tarea,
                ),
            )

        conn.commit()

    except Exception as error:
        conn.rollback()
        print(f"Error -> {error}")
        session["error_editar"] = "Error al actualizar la tarea"
        session["id_tarea"] = id_tarea
        return redirect(url_for("main_editar"))
    finally:
        conn.close()

    session.pop("id_tarea", None)
    return redirect(url_for("main"))

@app.route("/registro")
def registro():
    error_registro = session.pop("error_registro", False)
    return render_template("registro.html", error_registro=error_registro)

@app.route("/registado", methods=["POST"])
def registado():
    nombre_saneado = html.escape(
        request.form.get("nombre", "").strip(), quote=True
    )
    apellido_saneado = html.escape(
        request.form.get("apellido", "").strip(), quote=True
    )
    email_saneado = request.form.get("email", "").strip()
    alias_raw = request.form.get("alias", "").strip().lower()
    alias_saneado = html.escape(alias_raw, quote=True)

    password_saneada = request.form.get("password", "")
    password2_saneada = request.form.get("password2", "")

    patron_alias = r"^[^\W\d_]+$"
    patron_pass = r"^[= \w]+$"

    if not alias_saneado or not re.match(patron_alias, alias_saneado):
        session["error_registro"] = (
            "El alias de usuario no es válido. Solo se permiten letras"
        )
        return redirect(url_for("registro"))

    if not password_saneada or not re.match(patron_pass, password_saneada):
        session["error_registro"] = (
            "La contraseña tendrá 8 caracteres como mínimo y 10 como máximo. Sólo puede contener letras, dígitos, espacios y el símbolo ="
        )
        return redirect(url_for("registro"))

    if password_saneada != password2_saneada:
        session["error_registro"] = "Las contraseñas no son iguales"
        return redirect(url_for("registro"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT alias_usuario FROM usuarios WHERE alias_usuario = %s",
                (alias_saneado,),
            )
            if cursor.fetchone():
                session["error_registro"] = "El alias de usuario ya existe"
                return redirect(url_for("registro"))

            if "imagen" not in request.files:
                session["error_registro"] = "No se ha recibido ningún archivo."
                return redirect(url_for("registro"))

            archivo = request.files["imagen"]
            if archivo.filename == "":
                session["error_registro"] = "Error al subir el archivo."
                return redirect(url_for("registro"))

            extensiones_permitidas = {"jpg", "jpeg", "png", "webp", "avif"}
            mimes_permitidos = {
                "image/jpeg",
                "image/png",
                "image/webp",
                "image/avif",
            }

            ext = (
                archivo.filename.rsplit(".", 1)[-1].lower()
                if "." in archivo.filename
                else ""
            )
            if (
                ext not in extensiones_permitidas
                or archivo.mimetype not in mimes_permitidos
            ):
                session["error_registro"] = (
                    "Formato no permitido o el archivo no es una imagen válida."
                )
                return redirect(url_for("registro"))

            nombre_unico = f"{alias_saneado}_{uuid.uuid4().hex[:8]}.{ext}"
            carpeta_destino = os.path.join(app.root_path, "static", "img_users")
            os.makedirs(carpeta_destino, exist_ok=True)
            archivo.save(os.path.join(carpeta_destino, nombre_unico))

            ruta_db = f"img_users/{nombre_unico}"

            password_encriptada = bcrypt.hashpw(
                password_saneada.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            sql_insert = """
                INSERT INTO usuarios (nombre_usuario, apellido_usuario, email_usuario, alias_usuario, password_user, img_ruta)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql_insert,
                (
                    nombre_saneado,
                    apellido_saneado,
                    email_saneado,
                    alias_saneado,
                    password_encriptada,
                    ruta_db,
                ),
            )

        conn.commit()

    except Exception as err:
        conn.rollback()
        print(f"Error en registro -> {err}")
        session["error_registro"] = f"Error al registrar usuario: {err}"
        return redirect(url_for("registro"))
    finally:
        conn.close()

    return redirect(url_for("index"))

@app.route("/main_usuario", methods=["GET", "POST"])
def main_usuario():
    if "alias" not in session:
        return redirect(url_for("index"))

    if request.method == "GET":
        return redirect(url_for("main"))

    id_usuario = request.form.get("id_usuario")

    alias = session.get("alias")
    img_ruta = session.get("img_ruta")
    error_add = session.pop("error_add", "")
    tarea_existe = session.pop("tarea_existe", "")

    datos = obtener_datos_dashboard(id_usuario=id_usuario)

    return render_template(
        "main.html",
        alias=alias,
        img_ruta=img_ruta,
        error_add=error_add,
        tarea_existe=tarea_existe,
        **datos,
    )

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    if "alias" not in session:
        return redirect(url_for("index"))

    alias = session.get("alias")
    img_ruta = session.get("img_ruta")
    mensaje = session.pop("mensaje", False)

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id_usuario, nombre_usuario, apellido_usuario, email_usuario FROM usuarios WHERE alias_usuario = %s"
            cursor.execute(sql, (alias,))
            resultado_datos = cursor.fetchone()
    finally:
        conn.close()

    if not resultado_datos:
        return redirect(url_for("index"))

    session["id"] = resultado_datos["id_usuario"]

    return render_template(
        "modificar.html",
        alias=alias,
        img_ruta=img_ruta,
        mensaje=mensaje,
        nombre_usuario=resultado_datos["nombre_usuario"],
        apellido_usuario=resultado_datos["apellido_usuario"],
        email_usuario=resultado_datos["email_usuario"],
    )

@app.route("/update_usuario", methods=["POST"])
def update_usuario():
    if "alias" not in session or "id" not in session:
        return redirect(url_for("index"))

    id_user = session["id"]
    alias_saneado = session["alias"]

    nombre_saneado = html.escape(
        request.form.get("nombre", "").strip(), quote=True
    )
    apellido_saneado = html.escape(
        request.form.get("apellido", "").strip(), quote=True
    )
    email_saneado = request.form.get("email", "").strip()

    password_saneada = request.form.get("password", "")
    password2_saneada = request.form.get("password2", "")

    patron_alias = r"^[^\W\d_]+$"
    patron_pass = r"^[= \w]+$"

    if not alias_saneado or not re.match(patron_alias, alias_saneado):
        session["mensaje"] = (
            "El alias de usuario no es válido. Solo se permiten letras"
        )
        return redirect(url_for("modificar"))

    if not password_saneada or not re.match(patron_pass, password_saneada):
        session["mensaje"] = (
            "La contraseña tendrá 8 caracteres como mínimo y 10 como máximo. Sólo puede contener letras, dígitos, espacios y el símbolo ="
        )
        return redirect(url_for("modificar"))

    if password_saneada != password2_saneada:
        session["mensaje"] = "Las contraseñas no son iguales"
        return redirect(url_for("modificar"))

    password_encriptada = bcrypt.hashpw(
        password_saneada.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    if "imagen" not in request.files:
        session["mensaje"] = "No se ha recibido ningún archivo."
        return redirect(url_for("modificar"))

    archivo = request.files["imagen"]
    if archivo.filename == "":
        session["mensaje"] = "Error al subir el archivo."
        return redirect(url_for("modificar"))

    extensiones_permitidas = {"jpg", "jpeg", "png", "webp", "avif"}
    mimes_permitidos = {"image/jpeg", "image/png", "image/webp", "image/avif"}

    ext = (
        archivo.filename.rsplit(".", 1)[-1].lower()
        if "." in archivo.filename
        else ""
    )
    if (
        ext not in extensiones_permitidas
        or archivo.mimetype not in mimes_permitidos
    ):
        session["mensaje"] = (
            "Formato no permitido o el archivo no es una imagen válida."
        )
        return redirect(url_for("modificar"))

    nombre_unico = f"{alias_saneado}_{uuid.uuid4().hex[:8]}.{ext}"
    carpeta_destino = os.path.join(app.root_path, "static", "img_users")
    os.makedirs(carpeta_destino, exist_ok=True)
    archivo.save(os.path.join(carpeta_destino, nombre_unico))

    ruta_db = f"img_users/{nombre_unico}"

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_update = """
                UPDATE usuarios 
                SET nombre_usuario = %s, apellido_usuario = %s, email_usuario = %s, 
                    password_user = %s, img_ruta = %s 
                WHERE id_usuario = %s
            """
            cursor.execute(
                sql_update,
                (
                    nombre_saneado,
                    apellido_saneado,
                    email_saneado,
                    password_encriptada,
                    ruta_db,
                    id_user,
                ),
            )
        conn.commit()

        session["img_ruta"] = ruta_db

    except Exception as err:
        conn.rollback()
        print(f"Error al actualizar usuario -> {err}")
        session["mensaje"] = f"Error en la base de datos: {err}"
        return redirect(url_for("modificar"))
    finally:
        conn.close()

    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)
    