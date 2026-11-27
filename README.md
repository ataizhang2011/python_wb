WorkingBetter - Task & Project Management System (Flask Edition)

WorkingBetter is a full-stack Kanban task and project management web application. Originally built in native PHP, this project has been fully refactored and migrated to Python (Flask) using a modular Blueprint architecture and SQLAlchemy ORM.
WorkingBetter es una aplicación web full-stack para la gestión de tareas y proyectos estilo Kanban. Desarrollada originalmente en PHP nativo, esta versión ha sido completamente refactorizada y migrada a Python (Flask) utilizando una arquitectura modular con Blueprints y SQLAlchemy ORM.

Key Features & Architecture Highlights | Características y Arquitectura

• Modular Blueprint Architecture | Arquitectura Modular (Blueprints): Decoupled routes into auth, tareas, and usuario modules for clean separation of concerns and scalability.
• SQLAlchemy ORM & N+1 Prevention | ORM y Optimización de Consultas: Replaced raw SQL queries with relational models (Usuario, Tarea, Proyecto, Tipo, Estado) utilizing joinedload for efficient eager loading.
• Cross-Language Password Compatibility | Compatibilidad de Contraseñas: Seamless authentication supporting legacy PHP $2y$ bcrypt hashes alongside standard $2b$ hashes.
• Secure File Uploads | Subida Segura de Archivos: Avatar validation by file extension and MIME type, UUID renaming, and automatic cleanup of previous profile images.
• Kanban Task Filtering | Filtrado Dinámico de Tareas: Categorizes tasks by department (Frontend, Backend, Diseño, Fotografía, Database) and supports filtering by assigned team member.

Tech Stack | Tecnologías Utilizadas

• Backend: Python 3, Flask, Flask-SQLAlchemy
• Database: MySQL (PyMySQL driver)
• Security: Bcrypt, Python-dotenv, Custom @login_required Decorators
• Frontend: HTML5, CSS3, Jinja2 Templates

Project Structure | Estructura del Proyecto

Local Setup & Installation | Instalación y Ejecución Local

1. Clone the repository | Clonar el repositorio

git clone https://github.com
cd workingbetter-flask

2. Create and activate a virtual environment | Crear y activar entorno virtual

python3 -m venv venv

# On macOS/Linux:

source venv/bin/activate

# On Windows:

venv\Scripts\activate

3. Install dependencies | Instalar dependencias

pip install -r requirements.txt

4. Configure environment variables | Configurar variables de entorno

Create a .env file in the root directory based on .env.example and fill in your MySQL credentials:

SECRET_KEY=your_super_secret_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=working_better

5. Run the application | Ejecutar la aplicación

python app.py
Open your browser and navigate to http://127.0.0.1:5000.

Migration Journey (PHP ➡️ Python)

This project demonstrates a complete backend modernization workflow:

1. Direct Translation: Porting procedural PHP logic and MySQL queries to Flask and PyMySQL.
2. Refactoring: Eliminating code duplication using Python decorators and helper functions.
3. Architecture & ORM: Restructuring into Flask Blueprints and migrating to SQLAlchemy models with transactional integrity.
