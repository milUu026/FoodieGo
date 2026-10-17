# import sqlite3
# import os
#
#
# class DatabaseConnection:
#     """Maneja la conexión con la base de datos SQLite."""
#     # Ruta al archivo .db (dentro de la carpeta database/)
#     DB_PATH = os.path.join(os.path.dirname(__file__), 'foodiego.db')
#
#     @classmethod
#     def get_connection(cls):
#         """Devuelve una conexión activa a la BD."""
#         return sqlite3.connect(cls.DB_PATH)
#
#     @classmethod
#     def execute_query(cls, query, params=()):
#         """Ejecuta una consulta SQL y devuelve el cursor."""
#         conn = cls.get_connection()
#         cursor = conn.cursor()
#         cursor.execute(query, params)
#         conn.commit()
#         return conn, cursor  # Devolvemos ambos para poder cerrar después
#
#     @classmethod
#     def initialize_tables(cls):
#         """Crea todas las tablas si no existen."""
#         # Aquí irá el script adaptado (lo veremos en la Fase 2)
#         pass
import sqlite3
import os


class DatabaseConnection:
    """Maneja la conexión con la base de datos SQLite."""

    # Ruta al archivo .db (dentro de la carpeta database/)
    DB_PATH = os.path.join(os.path.dirname(__file__), 'foodiego.db')

    @classmethod
    def get_connection(cls):
        """Devuelve una conexión activa a la BD."""
        return sqlite3.connect(cls.DB_PATH)

    @classmethod
    def execute_query(cls, query, params=()):
        """Ejecuta una consulta SQL y devuelve el cursor."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return conn, cursor  # Devolvemos ambos para poder cerrar después

    @classmethod
    def initialize_tables(cls):
        """Crea todas las tablas si no existen."""
        conn = cls.get_connection()
        cursor = conn.cursor()

        # Script adaptado a SQLite
        queries = [
            '''CREATE TABLE IF NOT EXISTS clientes ( 
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT NOT NULL, 
                apellido TEXT NOT NULL, 
                email TEXT UNIQUE NOT NULL, 
                telefono TEXT, 
                direccion_entrega TEXT NOT NULL, 
                fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP 
            )''',

            '''CREATE TABLE IF NOT EXISTS restaurantes ( 
                id_restaurante INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT NOT NULL, 
                tipo_cocina TEXT, 
                direccion TEXT NOT NULL, 
                telefono TEXT, 
                calificacion_promedio REAL DEFAULT 0.0 
            )''',

            '''CREATE TABLE IF NOT EXISTS repartidores ( 
                id_repartidor INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT NOT NULL, 
                apellido TEXT NOT NULL, 
                tipo_vehiculo TEXT, 
                placa TEXT UNIQUE, 
                estado TEXT DEFAULT 'disponible' 
            )''',

            '''CREATE TABLE IF NOT EXISTS pedidos ( 
                id_pedido INTEGER PRIMARY KEY AUTOINCREMENT, 
                id_cliente INTEGER NOT NULL, 
                id_restaurante INTEGER NOT NULL, 
                id_repartidor INTEGER, 
                fecha_pedido TEXT DEFAULT CURRENT_TIMESTAMP, 
                estado TEXT DEFAULT 'pendiente', 
                total REAL NOT NULL, 
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente), 
                FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id_restaurante), 
                FOREIGN KEY (id_repartidor) REFERENCES repartidores(id_repartidor) 
            )'''
        ]

        for query in queries:
            cursor.execute(query)

        conn.commit()
        conn.close()
        print("✅ Tablas creadas correctamente")