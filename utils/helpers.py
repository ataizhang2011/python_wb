import os
import uuid
from flask import current_app
from models import Proyecto, db


def guardar_avatar(archivo, alias, ruta_anterior=None):
    """Valida y guarda el avatar, elimina automáticamente el avatar anterior y devuelve (nueva ruta, mensaje de error)"""
    if not archivo or archivo.filename == "":
        return None, "Error al subir el archivo."

    extensiones_permitidas = {"jpg", "jpeg", "png", "webp", "avif"}
    mimes_permitidos = {"image/jpeg", "image/png", "image/webp", "image/avif"}

    ext = (
        archivo.filename.rsplit(".", 1)[-1].lower()
        if "." in archivo.filename
        else ""
    )
    if ext not in extensiones_permitidas or archivo.mimetype not in mimes_permitidos:
        return None, "Formato no permitido o el archivo no es una imagen válida."

    nombre_unico = f"{alias}_{uuid.uuid4().hex[:8]}.{ext}"
    carpeta_destino = os.path.join(current_app.root_path, "static", "img_users")
    os.makedirs(carpeta_destino, exist_ok=True)
    archivo.save(os.path.join(carpeta_destino, nombre_unico))

    if ruta_anterior:
        ruta_completa_anterior = os.path.join(
            current_app.root_path, "static", ruta_anterior
        )
        if os.path.exists(ruta_completa_anterior):
            os.remove(ruta_completa_anterior)

    return f"img_users/{nombre_unico}", None


def obtener_o_crear_proyecto(nombre_proyecto):
    """Busca el ID del elemento; si no existe, insértalo automáticamente y devuelve el nuevo ID."""
    proyecto = Proyecto.query.filter_by(nombre_proyecto=nombre_proyecto).first()
    if proyecto:
        return proyecto.id_proyecto

    nuevo_proyecto = Proyecto(nombre_proyecto=nombre_proyecto)
    db.session.add(nuevo_proyecto)
    db.session.flush()
    return nuevo_proyecto.id_proyecto



# import os
# import uuid
# from flask import current_app

# def guardar_avatar(archivo, alias, ruta_anterior=None):
#     """Valida y guarda el avatar, elimina automáticamente el avatar anterior y devuelve (nueva ruta, mensaje de error)"""
#     if not archivo or archivo.filename == "":
#         return None, "Error al subir el archivo."

#     extensiones_permitidas = {"jpg", "jpeg", "png", "webp", "avif"}
#     mimes_permitidos = {"image/jpeg", "image/png", "image/webp", "image/avif"}

#     ext = archivo.filename.rsplit(".", 1)[-1].lower() if "." in archivo.filename else ""
#     if ext not in extensiones_permitidas or archivo.mimetype not in mimes_permitidos:
#         return None, "Formato no permitido o el archivo no es una imagen válida."

#     nombre_unico = f"{alias}_{uuid.uuid4().hex[:8]}.{ext}"
#     carpeta_destino = os.path.join(current_app.root_path, "static", "img_users")
#     os.makedirs(carpeta_destino, exist_ok=True)
#     archivo.save(os.path.join(carpeta_destino, nombre_unico))

#     if ruta_anterior:
#         ruta_completa_anterior = os.path.join(current_app.root_path, "static", ruta_anterior)
#         if os.path.exists(ruta_completa_anterior):
#             os.remove(ruta_completa_anterior)

#     return f"img_users/{nombre_unico}", None

# def obtener_o_crear_proyecto(cursor, nombre_proyecto):
#     """Busca el ID del elemento; si no existe, insértalo automáticamente y devuelve el nuevo ID."""
#     cursor.execute(
#         "SELECT id_proyecto FROM proyectos WHERE nombre_proyecto = %s",
#         (nombre_proyecto,),
#     )
#     row = cursor.fetchone()
#     if row:
#         return row["id_proyecto"]

#     cursor.execute(
#         "INSERT INTO proyectos (nombre_proyecto) VALUES (%s)",
#         (nombre_proyecto,),
#     )
#     return cursor.lastrowid
