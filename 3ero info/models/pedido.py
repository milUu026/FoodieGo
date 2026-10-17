from models.base_model import Model
from database.connection import DatabaseConnection


class Pedido(Model):
    """Modelo que representa la tabla 'pedidos' - la tabla central."""

    table_name = "pedidos"
    primary_key = "id_pedido"
    fields = ["id_cliente", "id_restaurante", "id_repartidor", "estado", "total"]

    def __init__(self, **kwargs):
        """Acepta cualquier campo de la tabla pedidos."""
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
        print(f"✅ Pedido #{self.id_pedido} creado")

    def get_cliente(self):
        """Obtiene el objeto Cliente asociado a este pedido."""
        from models.cliente import Cliente
        return Cliente.find_by_id(self.id_cliente)

    def get_restaurante(self):
        """Obtiene el objeto Restaurante asociado a este pedido."""
        from models.restaurante import Restaurante
        return Restaurante.find_by_id(self.id_restaurante)

    def get_repartidor(self):
        """Obtiene el objeto Repartidor asignado (puede ser None)."""
        if self.id_repartidor is None:
            return None

        from models.repartidor import Repartidor
        return Repartidor.find_by_id(self.id_repartidor)

    def detalles_pedido(self):
        """Muestra información completa del pedido con nombres en lugar de IDs."""
        cliente = self.get_cliente()
        restaurante = self.get_restaurante()
        repartidor = self.get_repartidor()

        print(f"\n{'=' * 50}")
        print(f"📦 PEDIDO #{self.id_pedido}")
        print(f"{'=' * 50}")
        print(f"👤 Cliente: {cliente.nombre} {cliente.apellido}")
        print(f"📍 Dirección: {cliente.direccion_entrega}")
        print(f"🍽️  Restaurante: {restaurante.nombre}")
        print(f"🍴 Tipo: {restaurante.tipo_cocina}")
        print(f"📅 Fecha: {self.fecha_pedido}")
        print(f"💰 Total: ${self.total}")
        print(f"📊 Estado: {self.estado.upper()}")

        if repartidor:
            print(f"🚴 Repartidor: {repartidor.nombre} {repartidor.apellido}")
            print(f" Vehículo: {repartidor.tipo_vehiculo} ({repartidor.placa})")
        else:
            print("🚴 Repartidor: Sin asignar")

        print(f"{'=' * 50}\n")