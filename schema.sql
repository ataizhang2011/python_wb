-- ==========================================
-- WorkingBetter Creación de tablas de base de datos y script de diccionario básico.
-- ==========================================

SET FOREIGN_KEY_CHECKS = 0;

-- 1. usuarios
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL,
    apellido_usuario VARCHAR(100),
    email_usuario VARCHAR(100) UNIQUE,
    alias_usuario VARCHAR(20) UNIQUE NOT NULL,
    password_user VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado INT DEFAULT 1,
    img_ruta VARCHAR(255)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 2. proyectos
DROP TABLE IF EXISTS proyectos;

CREATE TABLE proyectos (
    id_proyecto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_proyecto VARCHAR(100) NOT NULL,
    descripcion_proyecto VARCHAR(300)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 3. tipos
DROP TABLE IF EXISTS tipos;

CREATE TABLE tipos (
    id_tipo INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(100) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 4. estados
DROP TABLE IF EXISTS estados;

CREATE TABLE estados (
    id_estado INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_estado VARCHAR(100) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 5. tareas
DROP TABLE IF EXISTS tareas;

CREATE TABLE tareas (
    id_tarea INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_tarea VARCHAR(100) NOT NULL,
    descripcion_tarea TEXT NOT NULL,
    id_proyecto INT NOT NULL,
    id_tipo INT NOT NULL,
    id_usuario INT NOT NULL,
    id_estado INT NOT NULL,
    fecha_ini TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actua TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_tareas_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_tareas_proyectos FOREIGN KEY (id_proyecto) REFERENCES proyectos (id_proyecto) ON DELETE CASCADE,
    CONSTRAINT fk_tareas_tipos FOREIGN KEY (id_tipo) REFERENCES tipos (id_tipo),
    CONSTRAINT fk_tareas_estados FOREIGN KEY (id_estado) REFERENCES estados (id_estado)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- ==========================================
-- Introduce los datos de diccionario fundamentales necesarios para el funcionamiento del sistema.
-- ==========================================
INSERT INTO
    tipos (nombre_tipo)
VALUES ('frontend'),
    ('backend'),
    ('diseñado'),
    ('fotografia'),
    ('database');

INSERT INTO
    estados (nombre_estado)
VALUES ('pendiente'),
    ('en curso'),
    ('finalizado');

INSERT INTO
    proyectos (
        nombre_proyecto,
        descripcion_proyecto
    )
VALUES (
        'workingbetter',
        'Un app para trabajarmos juntos mejor'
    ),
    (
        'color',
        'Un app para practicar desarrollo web'
    );