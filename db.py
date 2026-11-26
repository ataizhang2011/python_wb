import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

def obtener_datos_dashboard(id_usuario=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_tareas = """
                SELECT t.id_tarea, t.nombre_tarea, p.nombre_proyecto, t.descripcion_tarea, 
                       tp.nombre_tipo, t.id_estado, t.id_usuario,
                       CONCAT(u.nombre_usuario, " ", u.apellido_usuario) AS assigned_to, 
                       u.alias_usuario, u.img_ruta, t.fecha_ini, t.fecha_actua, e.nombre_estado
                FROM tareas t
                NATURAL JOIN proyectos p
                NATURAL JOIN tipos tp
                NATURAL JOIN usuarios u
                NATURAL JOIN estados e
            """
            if id_usuario:
                sql_tareas += " WHERE u.id_usuario = %s"
                cursor.execute(sql_tareas, (id_usuario,))
            else:
                cursor.execute(sql_tareas)

            todas_tareas = cursor.fetchall()

            sql_usuarios = """
                SELECT id_usuario, CONCAT(nombre_usuario, " ", apellido_usuario) AS usuario, img_ruta
                FROM usuarios
            """
            cursor.execute(sql_usuarios)
            usuarios = cursor.fetchall()

    finally:
        conn.close()

    tareas_frontend = [
        t for t in todas_tareas if t["nombre_tipo"].lower() == "frontend"
    ]
    tareas_backend = [
        t for t in todas_tareas if t["nombre_tipo"].lower() == "backend"
    ]
    tareas_dise = [
        t for t in todas_tareas if t["nombre_tipo"].lower() == "diseñado"
    ]
    tareas_fotos = [
        t for t in todas_tareas if t["nombre_tipo"].lower() == "fotografia"
    ]
    tareas_database = [
        t for t in todas_tareas if t["nombre_tipo"].lower() == "database"
    ]

    return {
        "tareas_frontend": tareas_frontend,
        "todo_frontend": len(tareas_frontend),
        "tareas_backend": tareas_backend,
        "todo_backend": len(tareas_backend),
        "tareas_dise": tareas_dise,
        "todo_dise": len(tareas_dise),
        "tareas_fotos": tareas_fotos,
        "todo_fotos": len(tareas_fotos),
        "tareas_database": tareas_database,
        "todo_database": len(tareas_database),
        "usuarios": usuarios,
    }

