# WorkingBetter (Versión Python / Flask)

Aplicación web de gestión de tareas estilo Kanban desarrollada originalmente en **PHP nativo (PDO)** y migrada completamente a **Python** utilizando el microframework **Flask**.

Este proyecto demuestra la transición arquitectónica desde scripts procedurales hacia una estructura modular MVC/MTV, optimizando consultas a bases de datos en la nube y aplicando buenas prácticas de seguridad.

---

## Características Principales

- **Autenticación y Gestión de Sesiones:** Registro de nuevos usuarios, inicio y cierre de sesión con protección de rutas mediante `session`.
- **Seguridad de Contraseñas:** Cifrado y verificación compatible con hashes de PHP (`$2y$` / `$2b$`) utilizando `bcrypt`.
- **Subida y Validación de Archivos:** Gestión de avatares de perfil con validación de extensiones, tipos MIME y generación de nombres únicos (`uuid`).
- **CRUD Completo de Tareas:**
  - **Create:** Creación de tareas con validación de duplicados y creación automática de proyectos nuevos.
  - **Read:** Tablero visual dividido en 5 categorías (_Frontend, Backend, Diseño, Fotografía, Base de datos_) con contadores dinámicos y filtrado por usuario.
  - **Update:** Edición en línea (_inline editing_) directamente desde la tarjeta de cada tarea, además de actualización de datos y avatar del perfil de usuario.
  - **Delete:** Eliminación segura de tareas con confirmación de transacción.

---

## Mejoras Técnicas respecto a la versión PHP

1. **Optimización de Consultas SQL:** En la versión original en PHP se realizaban 11 consultas independientes para obtener las tareas y contadores por categoría. En Python se redujo a **una única consulta `JOIN`** y se agruparon los resultados en memoria mediante _List Comprehensions_, reduciendo drásticamente la latencia con la base de datos remota.
2. **Separación de Responsabilidades:** División clara entre la lógica de negocio (`app.py`), la capa de acceso a datos (`db.py`) y la presentación mediante el motor de plantillas **Jinja2** (`templates/`).
3. **Gestión de Transacciones:** Implementación de `commit()` y `rollback()` explícitos para garantizar la integridad de los datos en operaciones múltiples.
4. **Variables de Entorno:** Desacoplamiento de credenciales sensibles mediante `python-dotenv` (`.env`).

---

## Tecnologías Utilizadas

- **Backend:** Python 3, Flask
- **Base de Datos:** MySQL (Clever Cloud), PyMySQL
- **Seguridad:** Bcrypt, Python-dotenv
- **Frontend:** HTML5, CSS3, JavaScript, Jinja2, Bootstrap Icons

---

## Estructura del Proyecto

```text
workingbetter_py/
├── static/                 # Archivos estáticos (CSS, JS, imágenes y avatares)
│   ├── css/
│   ├── js/
│   └── img_users/
├── templates/              # Plantillas HTML con sintaxis Jinja2
│   ├── index.html          # Página de inicio de sesión
│   ├── registro.html       # Formulario de registro
│   ├── main.html           # Tablero principal de tareas
│   ├── modificar.html      # Edición de perfil de usuario
│   └── ...                 # Componentes reutilizables (header, footer, tarjetas)
├── app.py                  # Rutas y controladores principales de Flask
├── db.py                   # Conexión a MySQL y consultas optimizadas
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no incluido en el repositorio)
└── .gitignore              # Archivos ignorados por Git
```

---

## Instalación y Ejecución Local

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com
   cd workingbetter-python
   ```

2. **Crear y activar un entorno virtual:**

   ```bash
   python3 -m venv venv
   # En macOS / Linux:
   source venv/bin/activate
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto con tus credenciales de MySQL:

   ```env
   DB_HOST=host_mysql
   DB_USER=usuario
   DB_PASSWORD=contraseña
   DB_NAME=nombre_base_datos
   SECRET_KEY=una_clave_secreta_segura
   ```

5. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```
   Abre tu navegador y accede a `http://127.0.0.1:5000`.
# python_wb
