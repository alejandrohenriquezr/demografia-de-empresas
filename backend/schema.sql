-- Catálogo MySQL para administrar los recursos publicados de la operación estadística.
CREATE TABLE categorias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  slug VARCHAR(80) NOT NULL UNIQUE,
  nombre VARCHAR(160) NOT NULL,
  seccion ENUM('publicaciones', 'documentacion') NOT NULL,
  orden INT NOT NULL DEFAULT 0
);

CREATE TABLE recursos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  categoria_id INT NOT NULL,
  titulo_publico VARCHAR(255) NOT NULL,
  nombre_archivo VARCHAR(255) NOT NULL UNIQUE,
  ruta_relativa VARCHAR(500) NOT NULL UNIQUE,
  tipo_archivo VARCHAR(30) NOT NULL,
  fecha_publicacion DATE NULL,
  estado ENUM('borrador', 'publicado', 'archivado') NOT NULL DEFAULT 'borrador',
  orden INT NOT NULL DEFAULT 0,
  creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_recursos_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

