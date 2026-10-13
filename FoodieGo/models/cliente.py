from models.base_model import Model
from database.connection import DatabaseConnection


class Cliente(Model):
    """Modelo que representa la tabla 'clientes'."""
    table_name = "clientes"
    primary_key = "id_cliente"  # FoodieGo usa id_cliente, no id
    fields = ["nombre", "apellido", "email", "telefono", "direccion_entrega"]

    def __init__(self, **kwargs):
        """Acepta cualquier campo de la tabla clientes."""
        super().__init__(**kwargs)  # Pasa todos los kwargs al padre

    def save(self):
        """INSERT: Guarda el cliente en la base de datos."""
        # Construir la consulta dinámicamente
        columns = ", ".join(self.fields)
        placeholders = ", ".join(["?" for _ in self.fields])
        values = tuple(getattr(self, field) for field in self.fields)

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        conn, cursor = DatabaseConnection.execute_query(query, values)

        # Guardar el id generado automáticamente
        self.id_cliente = cursor.lastrowid
        conn.close()

        print(f"✅ Cliente {self.nombre} guardado con ID {self.id_cliente}")