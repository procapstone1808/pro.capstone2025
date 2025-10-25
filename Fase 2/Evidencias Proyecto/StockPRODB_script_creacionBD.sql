/* ======= CATÁLOGOS BÁSICOS ======= */
CREATE TABLE sp_estado_proceso (
  estado_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  codigo           VARCHAR2(30) UNIQUE NOT NULL,   -- INICIADO,PROMESA,ESCRITURA,INSCRITA,DESISTIDA
  nombre           VARCHAR2(80) NOT NULL
);

CREATE TABLE sp_tipo_documento (
  tipo_doc_id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  codigo           VARCHAR2(40) UNIQUE NOT NULL,   -- PROMESA,ESCRITURA,INSCRIPCION_CBR,DOMINIO_VIGENTE,OTROS
  nombre           VARCHAR2(120) NOT NULL,
  requiere_notaria CHAR(1) DEFAULT 'N' CHECK (requiere_notaria IN ('Y','N')),
  requiere_cbr     CHAR(1) DEFAULT 'N' CHECK (requiere_cbr     IN ('Y','N'))
);

CREATE TABLE sp_organismo (
  organismo_id     NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tipo             VARCHAR2(20) NOT NULL CHECK (tipo IN ('NOTARIA','CBR')),
  nombre           VARCHAR2(160) NOT NULL,
  comuna           VARCHAR2(80),
  region           VARCHAR2(80)
);

/* ======= USUARIOS DEL SISTEMA (corredores) ======= */
CREATE TABLE sp_usuario (
  usuario_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rut          VARCHAR2(12)  NOT NULL,           -- 12.345.678-9
  nombre       VARCHAR2(120) NOT NULL,
  email        VARCHAR2(120) NOT NULL UNIQUE,
  telefono     VARCHAR2(20),
  rol          VARCHAR2(20)  NOT NULL,           -- ADMIN|CORREDOR
  pass         VARCHAR2(30) NOT NULL,
  is_active    CHAR(1) DEFAULT 'Y' CHECK (is_active IN ('Y','N'))
);
CREATE UNIQUE INDEX ux_usuario_rut ON sp_usuario(rut);

/* ======= PROPIEDADES ======= */
CREATE TABLE sp_propiedad (
  propiedad_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rol_sii             VARCHAR2(20) NOT NULL,
  direccion           VARCHAR2(200) NOT NULL,
  comuna              VARCHAR2(80)  NOT NULL,
  region              VARCHAR2(80)  NOT NULL,
  tipo                VARCHAR2(20)  NOT NULL,     -- CASA|DEPTO|OFICINA|LOCAL|ETC
  sup_construida_m2   NUMBER(10,2),
  sup_terreno_m2      NUMBER(10,2),
  dormitorios         NUMBER(2),
  banos               NUMBER(2),
  estacionamientos    NUMBER(2),
  estado              VARCHAR2(20) DEFAULT 'DISPONIBLE', -- DISPONIBLE|VENDIDA|ARRENDADA
  precio_ref_clp      NUMBER(14,2)
);
CREATE UNIQUE INDEX ux_propiedad_rol ON sp_propiedad(rol_sii);

/* ======= PROCESO DE VENTA ======= */
CREATE TABLE sp_proceso_venta (
  venta_id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  propiedad_id     NUMBER NOT NULL,
  corredor_id      NUMBER NOT NULL,                 -- sp_usuario
  estado_id        NUMBER NOT NULL,                 -- sp_estado_proceso
  fecha_inicio     DATE   NOT NULL,
  fecha_cierre     DATE,
  precio_uf        NUMBER(12,2),
  precio_clp       NUMBER(14,2),
  comision_uf      NUMBER(12,2),
  comision_clp     NUMBER(14,2),
  CONSTRAINT fk_venta_propiedad  FOREIGN KEY (propiedad_id) REFERENCES sp_propiedad(propiedad_id),
  CONSTRAINT fk_venta_corredor   FOREIGN KEY (corredor_id)  REFERENCES sp_usuario(usuario_id),
  CONSTRAINT fk_venta_estado     FOREIGN KEY (estado_id)    REFERENCES sp_estado_proceso(estado_id)
);
CREATE INDEX ix_venta_propiedad ON sp_proceso_venta(propiedad_id);
CREATE INDEX ix_venta_corredor  ON sp_proceso_venta(corredor_id);

/* ======= PARTES DEL PROCESO (Compradores/Vendedores) ======= */
CREATE TABLE sp_persona (
  persona_id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rut             VARCHAR2(12) NOT NULL,
  nombre          VARCHAR2(160) NOT NULL,
  email           VARCHAR2(120),
  telefono        VARCHAR2(20),
  tipo_persona    VARCHAR2(10) DEFAULT 'NATURAL' CHECK (tipo_persona IN ('NATURAL','JURIDICA'))
);
CREATE UNIQUE INDEX ux_persona_rut ON sp_persona(rut);

CREATE TABLE sp_parte_proceso (
  venta_id      NUMBER NOT NULL,
  persona_id    NUMBER NOT NULL,
  rol_parte     VARCHAR2(12) NOT NULL CHECK (rol_parte IN ('COMPRADOR','VENDEDOR')),
  share_percent NUMBER(5,2),
  CONSTRAINT pk_parte_proceso PRIMARY KEY (venta_id, persona_id, rol_parte),
  CONSTRAINT fk_pp_venta   FOREIGN KEY (venta_id)   REFERENCES sp_proceso_venta(venta_id),
  CONSTRAINT fk_pp_persona FOREIGN KEY (persona_id) REFERENCES sp_persona(persona_id)
);

/* ======= DOCUMENTOS + VERSIONADO (para el editor) ======= */
CREATE TABLE sp_documento (
  documento_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  venta_id       NUMBER NOT NULL,
  tipo_doc_id    NUMBER NOT NULL,
  organismo_id   NUMBER,                           -- Notaría/CBR cuando aplique
  estado_doc     VARCHAR2(20),                     -- BORRADOR|FIRMADO|PROTOCOLIZADO|INSCRITO
  costo_clp      NUMBER(14,2),
  fecha_doc      DATE,
  CONSTRAINT fk_doc_venta     FOREIGN KEY (venta_id)     REFERENCES sp_proceso_venta(venta_id),
  CONSTRAINT fk_doc_tipo      FOREIGN KEY (tipo_doc_id)  REFERENCES sp_tipo_documento(tipo_doc_id),
  CONSTRAINT fk_doc_organismo FOREIGN KEY (organismo_id) REFERENCES sp_organismo(organismo_id)
);
CREATE INDEX ix_doc_venta ON sp_documento(venta_id);

CREATE TABLE sp_documento_version (
  doc_version_id  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  documento_id    NUMBER NOT NULL,
  creado_por      NUMBER NOT NULL,        -- sp_usuario
  creado_en       DATE DEFAULT SYSDATE,
  html_contenido  CLOB,                   -- lo que editas en CKEditor/Quill
  archivo_pdf_url  VARCHAR2(1000),
  archivo_docx_url VARCHAR2(1000),
  CONSTRAINT fk_docv_doc   FOREIGN KEY (documento_id) REFERENCES sp_documento(documento_id),
  CONSTRAINT fk_docv_user  FOREIGN KEY (creado_por)   REFERENCES sp_usuario(usuario_id)
);

/* ======= ASIGNACIÓN DE PERMISOS POR PROPIEDAD ======= */
CREATE TABLE sp_asignacion_propiedad (
  propiedad_id  NUMBER NOT NULL,
  usuario_id    NUMBER NOT NULL,
  permiso       VARCHAR2(10) NOT NULL CHECK (permiso IN ('VER','EDITAR','ADMIN')),
  CONSTRAINT pk_asig_prop PRIMARY KEY (propiedad_id, usuario_id),
  CONSTRAINT fk_asig_prop_prop FOREIGN KEY (propiedad_id) REFERENCES sp_propiedad(propiedad_id),
  CONSTRAINT fk_asig_prop_user FOREIGN KEY (usuario_id)   REFERENCES sp_usuario(usuario_id)
);

COMMIT;
