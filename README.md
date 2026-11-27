
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
<img width="658" height="358" alt="architecture" src="https://github.com/user-attachments/assets/d333306e-1705-4675-90b1-ecdf725b2865" />WorkingBetter - Task & Project Management System (Flask Edition)

![Uploading ar<svg class="light" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 658 358" width="658" height="358" id="m0e6f38__root" data-diagram-type="ascii">
  <style data-mercat-style="universal">.mercat text{font-family:'Google Sans',Roboto,Arial,sans-serif;fill:var(--m-text);dominant-baseline:central}.mercat .m-edge .m-path{fill:none;stroke:var(--m-line);stroke-width:1.5px}.mercat .m-note .m-label{fill:var(--m-note-text)}.mercat .t-label{font-size:13px;font-weight:500}</style>
  <style data-mercat-style="theme-light">#m0e6f38__root{--m-text:#1f1f1f;--m-line:#545454;--m-note-text:#1f1f1f}</style>
  <style data-mercat-style="theme-dark">#m0e6f38__root.dark{--m-text:#e3e3e3;--m-line:#bfbfbf;--m-note-text:#e3e3e3}</style>
  <style data-mercat-style="type">#m0e6f38__root .bus-line{fill:none;stroke:var(--m-line);stroke-width:1.5px;stroke-linecap:round;stroke-linejoin:round}#m0e6f38__root .annotation-text{fill:var(--m-text);font-size:13px;font-weight:500;white-space:pre}</style>
  <style data-mercat-style="diagram">#m0e6f38__root text{font-family:Google Sans Mono, Roboto Mono, monospace}</style>
  <g class="mercat mercat-ascii">
    <g class="m-edge" id="m0e6f38__edge__pt__a1__0" data-role="connector">
      <line x1="19.25" y1="47" x2="36.25" y2="47" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a3__0" data-role="connector">
      <line x1="19.25" y1="69" x2="36.25" y2="69" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a5__0" data-role="connector">
      <line x1="19.25" y1="91" x2="36.25" y2="91" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a7__0" data-role="connector">
      <line x1="19.25" y1="113" x2="36.25" y2="113" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a8__0" data-role="connector">
      <line x1="53.25" y1="135" x2="70.25" y2="135" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a10__0" data-role="connector">
      <line x1="53.25" y1="157" x2="70.25" y2="157" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a12__0" data-role="connector">
      <line x1="53.25" y1="179" x2="70.25" y2="179" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a14__0" data-role="connector">
      <line x1="19.25" y1="201" x2="36.25" y2="201" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a15__0" data-role="connector">
      <line x1="53.25" y1="223" x2="70.25" y2="223" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a17__0" data-role="connector">
      <line x1="53.25" y1="245" x2="70.25" y2="245" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a19__0" data-role="connector">
      <line x1="19.25" y1="267" x2="36.25" y2="267" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a21__0" data-role="connector">
      <line x1="19.25" y1="289" x2="36.25" y2="289" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a23__0" data-role="connector">
      <line x1="19.25" y1="311" x2="36.25" y2="311" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__a25__0" data-role="connector">
      <line x1="19.25" y1="333" x2="36.25" y2="333" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__pt__0" data-role="connector">
      <line x1="19.25" y1="47" x2="19.25" y2="333" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__pt__1" data-role="connector">
      <line x1="53.25" y1="135" x2="53.25" y2="179" class="m-path bus-line"/>
    </g>
    <g class="m-edge" id="m0e6f38__edge__pt__pt__2" data-role="connector">
      <line x1="53.25" y1="223" x2="53.25" y2="245" class="m-path bus-line"/>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a0" data-role="annotation">
      <text x="15" y="25" class="m-label t-label annotation-text" text-anchor="start">workingbetter_py/</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a1" data-role="annotation">
      <text x="49" y="47" class="m-label t-label annotation-text" text-anchor="start">app.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a2" data-role="annotation">
      <text x="253" y="47" class="m-label t-label annotation-text" text-anchor="start"># Application entry point &amp; Blueprint registration</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a3" data-role="annotation">
      <text x="49" y="69" class="m-label t-label annotation-text" text-anchor="start">models.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a4" data-role="annotation">
      <text x="253" y="69" class="m-label t-label annotation-text" text-anchor="start"># SQLAlchemy database models &amp; relationships</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a5" data-role="annotation">
      <text x="49" y="91" class="m-label t-label annotation-text" text-anchor="start">db.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a6" data-role="annotation">
      <text x="253" y="91" class="m-label t-label annotation-text" text-anchor="start"># Dashboard data aggregation &amp; query logic</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a7" data-role="annotation">
      <text x="49" y="113" class="m-label t-label annotation-text" text-anchor="start">routes/</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a8" data-role="annotation">
      <text x="83" y="135" class="m-label t-label annotation-text" text-anchor="start">auth.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a9" data-role="annotation">
      <text x="253" y="135" class="m-label t-label annotation-text" text-anchor="start"># Authentication (login, register, logout)</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a10" data-role="annotation">
      <text x="83" y="157" class="m-label t-label annotation-text" text-anchor="start">tareas.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a11" data-role="annotation">
      <text x="253" y="157" class="m-label t-label annotation-text" text-anchor="start"># Task CRUD operations &amp; Kanban board</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a12" data-role="annotation">
      <text x="83" y="179" class="m-label t-label annotation-text" text-anchor="start">usuario.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a13" data-role="annotation">
      <text x="253" y="179" class="m-label t-label annotation-text" text-anchor="start"># User profile updates &amp; user-specific filtering</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a14" data-role="annotation">
      <text x="49" y="201" class="m-label t-label annotation-text" text-anchor="start">utils/</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a15" data-role="annotation">
      <text x="83" y="223" class="m-label t-label annotation-text" text-anchor="start">decorators.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a16" data-role="annotation">
      <text x="253" y="223" class="m-label t-label annotation-text" text-anchor="start"># Session authentication decorators</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a17" data-role="annotation">
      <text x="83" y="245" class="m-label t-label annotation-text" text-anchor="start">helpers.py</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a18" data-role="annotation">
      <text x="253" y="245" class="m-label t-label annotation-text" text-anchor="start"># Avatar upload/cleanup &amp; project helper functions</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a19" data-role="annotation">
      <text x="49" y="267" class="m-label t-label annotation-text" text-anchor="start">static/</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a20" data-role="annotation">
      <text x="253" y="267" class="m-label t-label annotation-text" text-anchor="start"># CSS, JS, and uploaded user avatars</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a21" data-role="annotation">
      <text x="49" y="289" class="m-label t-label annotation-text" text-anchor="start">templates/</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a22" data-role="annotation">
      <text x="253" y="289" class="m-label t-label annotation-text" text-anchor="start"># Jinja2 HTML views</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a23" data-role="annotation">
      <text x="49" y="311" class="m-label t-label annotation-text" text-anchor="start">.env.example</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a24" data-role="annotation">
      <text x="253" y="311" class="m-label t-label annotation-text" text-anchor="start"># Environment variables template</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a25" data-role="annotation">
      <text x="49" y="333" class="m-label t-label annotation-text" text-anchor="start">requirements.txt</text>
    </g>
    <g class="m-node m-note" id="m0e6f38__note__a26" data-role="annotation">
      <text x="253" y="333" class="m-label t-label annotation-text" text-anchor="start"># Python dependencies</text>
    </g>
  </g>
</svg>
chitecture..svg…]()

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
