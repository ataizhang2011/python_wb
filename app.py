import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from flask import Flask
from models import db
from routes.auth import auth_bp
from routes.tareas import tareas_bp
from routes.usuario import usuario_bp
from routes.api import api_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "working_better_secret_key_change_me")

# Construye la URI de conexión a MySQL (utilizando `quote_plus` para evitar errores causados ​​por caracteres especiales en la contraseña)
db_user = os.getenv("DB_USER")
db_pass = quote_plus(os.getenv("DB_PASSWORD", ""))
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
# Registrar tres planes de negocio
app.register_blueprint(auth_bp)
app.register_blueprint(tareas_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(api_bp)

# Capa de compatibilidad: mantener operativos los endpoints `url_for` heredados en las plantillas
for rule in list(app.url_map.iter_rules()):
    if "." in rule.endpoint:
        short_name = rule.endpoint.split(".", 1)[1]
        if short_name not in app.view_functions:
            app.add_url_rule(
                rule.rule,
                endpoint=short_name,
                view_func=app.view_functions[rule.endpoint],
                methods=rule.methods,
            )

if __name__ == "__main__":
    app.run(debug=True)
