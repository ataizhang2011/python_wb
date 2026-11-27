from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    apellido_usuario = db.Column(db.String(100), nullable=False)
    email_usuario = db.Column(db.String(150), nullable=False)
    alias_usuario = db.Column(db.String(100), unique=True, nullable=False)
    password_user = db.Column(db.String(255), nullable=False)
    img_ruta = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, server_default=db.func.now())
    estado = db.Column(db.Integer, default=1)

    tareas = db.relationship("Tarea", back_populates="usuario")

    

    @property
    def usuario(self):
        return f"{self.nombre_usuario} {self.apellido_usuario}"


class Proyecto(db.Model):
    __tablename__ = "proyectos"

    id_proyecto = db.Column(db.Integer, primary_key=True)
    nombre_proyecto = db.Column(db.String(150), unique=True, nullable=False)
    descripcion_proyecto = db.Column(db.String(300))

    tareas = db.relationship("Tarea", back_populates="proyecto")


class Tipo(db.Model):
    __tablename__ = "tipos"

    id_tipo = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(100), nullable=False)

    tareas = db.relationship("Tarea", back_populates="tipo")


class Estado(db.Model):
    __tablename__ = "estados"

    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(100), nullable=False)

    tareas = db.relationship("Tarea", back_populates="estado")


class Tarea(db.Model):
    __tablename__ = "tareas"

    id_tarea = db.Column(db.Integer, primary_key=True)
    nombre_tarea = db.Column(db.String(150), unique=True, nullable=False)
    descripcion_tarea = db.Column(db.Text, nullable=False)
    id_proyecto = db.Column(db.Integer, db.ForeignKey("proyectos.id_proyecto"), nullable=False)
    id_tipo = db.Column(db.Integer, db.ForeignKey("tipos.id_tipo"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey("estados.id_estado"), nullable=False)
    fecha_ini = db.Column(db.DateTime, server_default=db.func.now())
    fecha_actua = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Afiliación/Relación
    proyecto = db.relationship("Proyecto", back_populates="tareas")
    tipo = db.relationship("Tipo", back_populates="tareas")
    usuario = db.relationship("Usuario", back_populates="tareas")
    estado = db.relationship("Estado", back_populates="tareas")

    # Atributos de compatibilidad: permiten que las plantillas HTML accedan directamente a los campos de las tablas asociadas sin necesidad de realizar modificaciones.
    @property
    def nombre_proyecto(self):
        return self.proyecto.nombre_proyecto

    @property
    def nombre_tipo(self):
        return self.tipo.nombre_tipo

    @property
    def nombre_estado(self):
        return self.estado.nombre_estado

    @property
    def assigned_to(self):
        return f"{self.usuario.nombre_usuario} {self.usuario.apellido_usuario}"

    @property
    def alias_usuario(self):
        return self.usuario.alias_usuario

    @property
    def img_ruta(self):
        return self.usuario.img_ruta
