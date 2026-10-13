from models.base_model import Model
from database.connection import DatabaseConnection


class Repartidor(Model):
    """Modelo que representa la tabla 'repartidores'."""
    table_name = "repartidores"
    primary_key = "id_repartidor"
    fields = ["nombre", "apellido", "tipo_vehiculo", "placa", "estado"]

    def __init__(self, **kwargs):
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

        print(f"✅ Repartidor {self.nombre} guardado con ID {self.id_repartidor}")

    def asignar_pedido(self, id_pedido):
        """Asigna este repartidor a un pedido específico."""
        query = f"UPDATE pedidos SET id_repartidor = ?, estado = 'en camino' WHERE id_pedido = ?"
        conn, cursor = DatabaseConnection.execute_query(query, (self.id_repartidor, id_pedido))
        conn.close()
        print(f"🚴 Pedido #{id_pedido} asignado a repartidor {self.nombre}")

    def get_pedidos_asignados(self):
        """Devuelve los pedidos asignados a este repartidor."""
        from models.pedido import Pedido
        query = "SELECT * FROM pedidos WHERE id_repartidor = ?"
        conn, cursor = DatabaseConnection.execute_query(query, (self.id_repartidor,))
        filas = cursor.fetchall()
        conn.close()

        pedidos = []
        columnas = [descripcion[0] for descripcion in cursor.description]
        for fila in filas:
            datos = dict(zip(columnas, fila))
            pedidos.append(Pedido(**datos))
        return pedidos