from models.base_model import Model
from database.connection import DatabaseConnection


class Restaurante(Model):
    """Modelo que representa la tabla 'restaurantes'."""
    table_name = "restaurantes"
    primary_key = "id_restaurante"
    fields = ["nombre", "tipo_cocina", "direccion", "telefono", "calificacion_promedio"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        """INSERT: Guarda el restaurante en la base de datos."""
        columns = ", ".join(self.fields)
        placeholders = ", ".join(["?" for _ in self.fields])
        values = tuple(getattr(self, field, None) for field in self.fields)

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        conn, cursor = DatabaseConnection.execute_query(query, values)
        self.id_restaurante = cursor.lastrowid
        conn.close()

        print(f"✅ Restaurante '{self.nombre}' guardado con ID {self.id_restaurante}")

    def get_pedidos(self):
        """Devuelve todos los pedidos asociados a este restaurante."""
        from models.pedido import Pedido
        query = "SELECT * FROM pedidos WHERE id_restaurante = ?"
        conn, cursor = DatabaseConnection.execute_query(query, (self.id_restaurante,))
        filas = cursor.fetchall()
        conn.close()

        pedidos = []
        columnas = [descripcion[0] for descripcion in cursor.description]
        for fila in filas:
            datos = dict(zip(columnas, fila))
            pedidos.append(Pedido(**datos))
        return pedidos