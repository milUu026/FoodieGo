from database.connection import DatabaseConnection

class Model:
    """Clase base de la que heredarán todos los modelos.

    Cada clase hija debe definir:
    - table_name: nombre de la tabla en la BD
    - fields: lista de campos (sin incluir el ID)
    - primary_key: nombre del campo ID
    """

    table_name = None  # Se define en cada clase hija
    fields = []  # Se define en cada clase hija
    primary_key = "id"  # Por defecto "id", se puede sobrescribir

    def __init__(self, **kwargs):
        """Recibe los atributos como argumentos con nombre."""
        for key, value in kwargs.items():
            setattr(self, key, value)  # Asigna dinámicamente los atributos

    def save(self):
        """Inserta o actualiza el objeto en la BD."""
        # Lo construiremos en la Fase 4
        pass

    @classmethod
    def all(cls):
        """Devuelve todos los registros de la tabla."""
        # Lo construiremos en la Fase 5
        pass

    # ... código anterior ...

    @classmethod
    def all(cls):
        """SELECT * FROM tabla → devuelve lista de objetos."""
        query = f"SELECT * FROM {cls.table_name}"
        conn, cursor = DatabaseConnection.execute_query(query)
        filas = cursor.fetchall()
        conn.close()

        # Convertir tuplas en objetos
        objetos = []
        columnas = [descripcion[0] for descripcion in cursor.description]

        for fila in filas:
            # Crear diccionario {nombre_columna: valor}
            datos = dict(zip(columnas, fila))
            # Instanciar el modelo con esos datos
            objeto = cls(**datos)
            objetos.append(objeto)

        return objetos

    @classmethod
    def find_by_id(cls, id_valor):
        """SELECT * FROM tabla WHERE pk = ? → devuelve un objeto o None."""
        query = f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = ?"
        conn, cursor = DatabaseConnection.execute_query(query, (id_valor,))
        fila = cursor.fetchone()
        conn.close()

        if fila:
            columnas = [descripcion[0] for descripcion in cursor.description]
            datos = dict(zip(columnas, fila))
            return cls(**datos)
        return None

    def update(self, **kwargs):
        """UPDATE: Modifica atributos específicos del objeto."""
        # Actualizar los atributos del objeto
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Construir el UPDATE
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [getattr(self, self.primary_key)]

        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary_key} = ?"

        conn, cursor = DatabaseConnection.execute_query(query, tuple(values))
        conn.close()
        print(f"✅ Registro {getattr(self, self.primary_key)} actualizado")

    def delete(self):
        """DELETE: Elimina el objeto de la BD."""
        id_valor = getattr(self, self.primary_key)
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"

        conn, cursor = DatabaseConnection.execute_query(query, (id_valor,))
        conn.close()
        print(f"️ Registro {id_valor} eliminado")