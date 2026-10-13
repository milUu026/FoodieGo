from models.base_model import Model
from database.connection import DatabaseConnection


class Pedido(Model):
    """Modelo que representa la tabla 'pedidos'."""
    table_name = "pedidos"
    primary_key = "id_pedido"
    fields = ["id_cliente", "id_restaurante", "id_repartidor", "estado", "total"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        """INSERT: Guarda el pedido en la base de datos."""
        columns = ", ".join(self.fields)
        placeholders = ", ".join(["?" for _ in self.fields])
        values = tuple(getattr(self, field, None) for field in self.fields)

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        conn, cursor = DatabaseConnection.execute_query(query, values)
        self.id_pedido = cursor.lastrowid
        conn.close()

        print(f"✅ Pedido #{self.id_pedido} guardado (Total: ${self.total})")

    def detalles_pedido(self):
        """Muestra los detalles completos del pedido formateados."""
        print(f"  - Pedido ID: {self.id_pedido}")
        print(f"    Estado: {self.estado}")
        print(f"    Total: ${self.total}")
        print(f"    Cliente ID: {self.id_cliente}")
        print(f"    Restaurante ID: {self.id_restaurante}")
        print(f"    Repartidor ID: {self.id_repartidor if self.id_repartidor else 'Sin asignar'}")