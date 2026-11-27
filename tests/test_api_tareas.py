import os
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

import bcrypt
import pytest
from app import app
from models import Estado, Proyecto, Tarea, Tipo, Usuario, db


@pytest.fixture
def client():
    """Configura el cliente de prueba y la base de datos en memoria."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = "test_secret_key"

    with app.app_context():
        db.engine.dispose()
        db.create_all()

        hashed_pw = bcrypt.hashpw(b"12345678", bcrypt.gensalt()).decode("utf-8")
        user = Usuario(
            nombre_usuario="richard",
            apellido_usuario="credriman",
            email_usuario="richard@gmail.com",
            alias_usuario="richard",
            password_user=hashed_pw,
            img_ruta="img_users/default.png",
        )
        tipo = Tipo(nombre_tipo="backend")
        estado_pendiente = Estado(nombre_estado="pendiente")
        estado_curso = Estado(nombre_estado="en curso")

        db.session.add_all([user, tipo, estado_pendiente, estado_curso])
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def auth_client(client):
    """Cliente autenticado con sesión iniciada para reutilizar en las pruebas."""
    client.post(
        "/api/login",
        json={"user": "richard", "pass": "12345678"},
    )
    return client



@pytest.fixture
def auth_client(client):
    """Un cliente de prueba que automatiza el proceso de inicio de sesión; el estado de inicio de sesión (sesión) establecido puede reutilizarse para pruebas de API posteriores."""
    client.post(
        "/api/login",
        json={"user": "richard", "pass": "12345678"},
    )
    return client


# ==========================================
# Sección de casos de prueba
# ==========================================

def test_unauthorized_access(client):
    """Verifica que, al intentar acceder a un endpoint protegido sin haber iniciado sesión, la solicitud sea interceptada y devuelva un 401."""
    res = client.get("/api/tareas")
    assert res.status_code == 401
    assert res.get_json()["status"] == "error"


def test_login_success_and_fail(client):
    """Prueba la API de inicio de sesión para los casos de inicio de sesión exitoso y de contraseña incorrecta."""
    # Contraseña incorrecta
    res_fail = client.post("/api/login", json={"user": "richard", "pass": "wrongpass"})
    assert res_fail.status_code == 401

    # Inicio de sesión correcto
    res_ok = client.post("/api/login", json={"user": "richard", "pass": "12345678"})
    assert res_ok.status_code == 200
    data = res_ok.get_json()
    assert data["status"] == "success"
    assert data["data"]["alias"] == "richard"


def test_crud_tareas_lifecycle(auth_client):
    """Incorporación de tareas de evaluación completas(POST) -> Consulta(GET) -> Revisar(PUT) -> borrar(DELETE)bucle cerrado"""
    # 1. Crear una nueva tarea (POST /api/tareas)
    payload = {
        "tarea": "Pytest Tareas de pruebas automatizadas",
        "proyecto": "workingbetter",
        "descripcion": "Verificación de flujos de trabajo CRUD mediante pytest",
        "tipo": "backend",
        "estado": "pendiente",
        "id_usuario": 1,
    }
    res_create = auth_client.post("/api/tareas", json=payload)
    assert res_create.status_code == 201
    created_data = res_create.get_json()["data"]
    task_id = created_data["id_tarea"]
    assert created_data["nombre_tarea"] == "Pytest Tareas de pruebas automatizadas"

    # 2. Obtener la lista de tareas y los detalles de cada tarea(GET /api/tareas & GET /api/tareas/<id>)
    res_list = auth_client.get("/api/tareas")
    assert res_list.status_code == 200
    assert res_list.get_json()["total"] == 1

    res_detail = auth_client.get(f"/api/tareas/{task_id}")
    assert res_detail.status_code == 200
    assert res_detail.get_json()["data"]["estado"] == "pendiente"

    # 3. Actualizar el estado y la descripción de la tarea (PUT /api/tareas/<id>)
    res_update = auth_client.put(
        f"/api/tareas/{task_id}",
        json={"estado": "en curso", "descripcion": "状态已变更为进行中"},
    )
    assert res_update.status_code == 200
    updated_data = res_update.get_json()["data"]
    assert updated_data["estado"] == "en curso"
    assert updated_data["descripcion_tarea"] == "状态已变更为进行中"

    # 4. borrar tarea (DELETE /api/tareas/<id>)
    res_delete = auth_client.delete(f"/api/tareas/{task_id}")
    assert res_delete.status_code == 200

    # Después de verificar la eliminación, una consulta posterior debería devolver 404
    res_after_delete = auth_client.get(f"/api/tareas/{task_id}")
    assert res_after_delete.status_code == 404


def test_create_duplicate_tarea(auth_client):
    """Al probar la creación de una tarea con un nombre que ya existe, el sistema debería interceptar la solicitud y devolver un código de estado 409 Conflict."""
    payload = {
        "tarea": "Nombre de tarea único",
        "proyecto": "workingbetter",
        "descripcion": "Creación inicial",
        "tipo": "backend",
        "estado": "pendiente",
        "id_usuario": 1,
    }
    auth_client.post("/api/tareas", json=payload)
    res_dup = auth_client.post("/api/tareas", json=payload)
    assert res_dup.status_code == 409
