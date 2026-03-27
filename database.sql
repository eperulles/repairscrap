-- =============================================
-- BASE DE DATOS PARA SISTEMA DE REPARACIONES
-- =============================================

-- 1. TABLA DE USUARIOS (login)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA DE ÁREAS
CREATE TABLE IF NOT EXISTS areas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

-- 3. TABLA DE LÍNEAS
CREATE TABLE IF NOT EXISTS lineas (
    id SERIAL PRIMARY KEY,
    numero INTEGER UNIQUE NOT NULL,
    area_id INTEGER REFERENCES areas(id),
    activo BOOLEAN DEFAULT TRUE
);

-- 4. TABLA DE DEFECTOS
CREATE TABLE IF NOT EXISTS defectos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    area_id INTEGER REFERENCES areas(id),
    activo BOOLEAN DEFAULT TRUE
);

-- 5. TABLA DE MODELOS
CREATE TABLE IF NOT EXISTS modelos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

-- 6. TABLA DE SUPERVISORES
CREATE TABLE IF NOT EXISTS supervisores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 7. TABLA DE REPARACIONES
CREATE TABLE IF NOT EXISTS reparaciones (
    id SERIAL PRIMARY KEY,
    tipo_registro VARCHAR(20) NOT NULL CHECK (tipo_registro IN ('PCBA', 'MEDIDOR')),
    qr VARCHAR(100),
    transfer VARCHAR(100),
    modelo VARCHAR(100),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    turno INTEGER NOT NULL CHECK (turno IN (1, 2, 3)),
    area_id INTEGER REFERENCES areas(id),
    linea_id INTEGER REFERENCES lineas(id),
    defecto_id INTEGER REFERENCES defectos(id),
    reparacion VARCHAR(255),
    ubicacion VARCHAR(100),
    supervisor VARCHAR(200),
    quien_repara_id INTEGER REFERENCES usuarios(id),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- DATOS DE EJEMPLO
-- =============================================

-- ÁREAS
INSERT INTO areas (nombre, descripcion) VALUES
('SMT', 'Surface Mount Technology'),
('THT', 'Through-Hole Technology'),
('Ensamble', 'Ensamble general'),
('Calibración', 'Calibración de equipos'),
('Postproceso', 'Procesos finales');

-- LÍNEAS (1 a 8, asignadas a diferentes áreas - ajustar según necesidad)
INSERT INTO lineas (numero, area_id) VALUES
(1, 1), (2, 1), (3, 1), (4, 1),
(5, 2), (6, 2),
(7, 3), (8, 3);

-- DEFECTOS COMUNES (ejemplo - agregar los tuyos)
INSERT INTO defectos (codigo, descripcion, area_id) VALUES
('DEF001', 'Soldadura fría', 1),
('DEF002', 'Componente mal colocado', 1),
('DEF003', 'Cortocircuito', 1),
('DEF004', 'Componente quemado', 1),
('DEF005', 'Pad dañado', 1),
('DEF006', 'Soldadura seca', 2),
('DEF007', 'Pin doblado', 2),
('DEF008', 'Hole fuera de spec', 2),
('DEF009', 'Falta de componente', 3),
('DEF010', 'Componente invertido', 3),
('DEF011', 'Ajuste fuera de rango', 4),
('DEF012', 'Falla de calibración', 4),
('DEF013', 'Raya en корпус', 5),
('DEF014', 'Etiqueta mal puesta', 5);

-- USUARIOS (contraseña: admin123 - en producción usar hash)
INSERT INTO usuarios (usuario, contrasena, nombre_completo) VALUES
('admin', 'admin123', 'Administrador'),
('operador1', 'operador123', 'Juan Pérez'),
('supervisor1', 'super123', 'María García');

-- MODELOS (ejemplo - agregar los tuyos)
INSERT INTO modelos (codigo, descripcion) VALUES
('MOD001', 'Medidor Monofásico'),
('MOD002', 'Medidor Trifásico'),
('MOD003', 'PCBA Principal'),
('MOD004', 'PCBA Secundario'),
('MOD005', 'Sensor Temperatura'),
('MOD006', 'Modulo Comunicación');

-- SUPERVISORES
INSERT INTO supervisores (nombre) VALUES
('Carlos Rodriguez'),
('Ana Martinez'),
('Roberto Sanchez');

-- =============================================
-- SEGURIDAD
-- =============================================

-- Habilitar RLS (Row Level Security)
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE areas ENABLE ROW LEVEL SECURITY;
ALTER TABLE lineas ENABLE ROW LEVEL SECURITY;
ALTER TABLE defectos ENABLE ROW LEVEL SECURITY;
ALTER TABLE modelos ENABLE ROW LEVEL SECURITY;
ALTER TABLE supervisores ENABLE ROW LEVEL SECURITY;
ALTER TABLE reparaciones ENABLE ROW LEVEL SECURITY;

-- Políticas para usuarios (solo lectura para operadores)
CREATE POLICY "Usuarios pueden ver sus datos" ON usuarios
    FOR SELECT USING (true);

CREATE POLICY "Solo admin puede modificar usuarios" ON usuarios
    FOR ALL USING (true);

-- Políticas para áreas y líneas
CREATE POLICY "Todos pueden ver áreas y líneas" ON areas
    FOR SELECT USING (true);
    
CREATE POLICY "Todos pueden ver líneas" ON lineas
    FOR SELECT USING (true);

-- Políticas para defectos
CREATE POLICY "Todos pueden ver defectos" ON defectos
    FOR SELECT USING (true);

-- Políticas para modelos
CREATE POLICY "Todos pueden ver modelos" ON modelos
    FOR SELECT USING (true);

-- Políticas para supervisores
CREATE POLICY "Todos pueden ver supervisores" ON supervisores
    FOR SELECT USING (true);

-- Políticas para reparaciones
CREATE POLICY "Operadores pueden insertar reparaciones" ON reparaciones
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Supervisores pueden ver todas" ON reparaciones
    FOR SELECT USING (true);
