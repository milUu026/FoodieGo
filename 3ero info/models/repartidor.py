from models.base_model import Model
from database.connection import DatabaseConnection


class Repartidor(Model):
    """Modelo que representa la tabla 'repartidores'."""

    table_name = "repartidores"
    primary_key = "id_repartidor"
    fields = ["nombre", "apellido", "tipo_vehiculo", "placa", "estado"]

    def __init__(self, **kwargs):
        """Acepta cualquier campo de la tabla repartidores."""
        super().__init__(**kwargs)

    def save(self):
        """INSERT: Guarda el repartidor en la base de datos."""
        columns = ", ".join(self.fields)
        placeholders = ", ".join(["?" for _ in self.fields])
        values = tuple(getattr(self, field, None) for field in self.fields)

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        conn, cursor = DatabaseConnection.execute_query(query, values)
        self.id_repartidor = cursor.lastrowid
        conn.close()
        print(f"✅ Repartidor '{self.nombre} {self.apellido}' guardado con ID {self.id_repartidor}")

    def get_pedidos_asignados(self):
        """Obtiene todos los pedidos asignados a este repartidor."""
        from models.pedido import Pedido

        query = """
            SELECT * FROM pedidos 
            WHERE id_repartidor = ?
            ORDER BY fecha_pedido DESC
        """

        conn, cursor = DatabaseConnection.execute_query(query, (self.id_repartidor,))
        filas = cursor.fetchall()
        columnas = [descripcion[0] for descripcion in cursor.description]
        conn.close()

        pedidos = []
        for fila in filas:
            datos = dict(zip(columnas, fila))
            pedido = Pedido(**datos)
            pedidos.append(pedido)

        return pedidos

    def asignar_pedido(self, id_pedido):
        """Asigna un pedido a este repartidor y cambia su estado a 'en_ruta'."""
        from models.pedido import Pedido

        # Actualizar el pedido
        query = """
            UPDATE pedidos 
            SET id_repartidor = ?, estado = 'en_camino'
            WHERE id_pedido = ?
        """

        conn, cursor = DatabaseConnection.execute_query(query, (self.id_repartidor, id_pedido))
        conn.close()
        print(f"✅ Pedido {id_pedido} asignado a {self.nombre}")

        # Actualizar estado del repartidor
        self.update(estado='en_ruta')