---- 1. Crear la base de datos
--CREATE DATABASE IF NOT EXISTS foodiego;
--
---- 2. Usar la base de datos
--USE foodiego;
--
---- 3. Creación de Tablas

-- Tabla de Clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion_entrega VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Restaurantes
CREATE TABLE restaurantes (
    id_restaurante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_cocina VARCHAR(50), -- Ej: Italiana, Mexicana, Fast Food
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    calificacion_promedio DECIMAL(2,1) DEFAULT 0.0
);

-- Tabla de Repartidores
CREATE TABLE repartidores (
    id_repartidor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    tipo_vehiculo VARCHAR(30), -- Ej: Moto, Bicicleta, Auto
    placa VARCHAR(20) UNIQUE,
    estado VARCHAR(20) DEFAULT 'disponible' -- disponible, en_ruta, desconectado
);

-- Tabla de Pedidos (La tabla central que relaciona a los actores)
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_restaurante INT NOT NULL,
    id_repartidor INT NULL, -- NULL porque al crear el pedido aún no se asigna repartidor
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente', -- pendiente, en_preparacion, en_camino, entregado, cancelado
    total DECIMAL(10,2) NOT NULL,

    -- Restricciones de Llaves Foráneas (Relaciones)
    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE RESTRICT,
    CONSTRAINT fk_pedido_restaurante
        FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id_restaurante) ON DELETE RESTRICT,
    CONSTRAINT fk_pedido_repartidor
        FOREIGN KEY (id_repartidor) REFERENCES repartidores(id_repartidor) ON DELETE SET NULL
);