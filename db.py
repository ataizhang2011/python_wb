from sqlalchemy.orm import joinedload
from models import Tarea, Usuario

def obtener_datos_dashboard(id_usuario=None):
    # Utiliza `joinedload` para cargar de forma anticipada las tablas relacionadas; su rendimiento es equivalente al de un `JOIN` de SQL nativo.
    query = Tarea.query.options(
        joinedload(Tarea.proyecto),
        joinedload(Tarea.tipo),
        joinedload(Tarea.usuario),
        joinedload(Tarea.estado),
    )

    if id_usuario:
        query = query.filter(Tarea.id_usuario == id_usuario)

    todas_tareas = query.all()
    usuarios = Usuario.query.all()

    tareas_frontend = [t for t in todas_tareas if t.nombre_tipo.lower() == "frontend"]
    tareas_backend = [t for t in todas_tareas if t.nombre_tipo.lower() == "backend"]
    tareas_dise = [t for t in todas_tareas if t.nombre_tipo.lower() == "diseñado"]
    tareas_fotos = [t for t in todas_tareas if t.nombre_tipo.lower() == "fotografia"]
    tareas_database = [t for t in todas_tareas if t.nombre_tipo.lower() == "database"]

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
