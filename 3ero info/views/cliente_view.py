
from tkinter import messagebox

from models.cliente import Cliente
from views.form_base import FormBase


class ClienteView(FormBase):
    """Interfaz para gestionar los clientes de FoodieGo."""

    titulo = "Gestión de Clientes"

    columnas_tabla = (
        "ID",
        "Nombre",
        "Apellido",
        "Email",
        "Teléfono",
        "Dirección de entrega"
    )

    ancho_columnas = (50, 120, 120, 180, 100, 220)

    campos_formulario = (
        {
            "nombre": "nombre",
            "etiqueta": "Nombre"
        },
        {
            "nombre": "apellido",
            "etiqueta": "Apellido"
        },
        {
            "nombre": "email",
            "etiqueta": "Correo electrónico"
        },
        {
            "nombre": "telefono",
            "etiqueta": "Teléfono"
        },
        {
            "nombre": "direccion_entrega",
            "etiqueta": "Dirección de entrega"
        }
    )

    def __init__(self, parent):
        super().__init__(parent, Cliente)

    def _obtener_datos_formulario(self):
        datos = {}

        for campo in self.campos_formulario:
            nombre = campo["nombre"]
            valor = self.entries[nombre].get().strip()
            datos[nombre] = valor

        # Validar campos obligatorios según el modelo y el esquema
        obligatorios = (
            "nombre",
            "apellido",
            "email",
            "direccion_entrega"
        )

        for campo in obligatorios:
            if not datos[campo]:
                messagebox.showwarning(
                    "Campo obligatorio",
                    f"El campo {campo.replace('_', ' ').capitalize()} "
                    "es obligatorio."
                )
                self.entries[campo].focus_set()
                return None

        if "@" not in datos["email"] or "." not in datos["email"]:
            messagebox.showwarning(
                "Correo inválido",
                "Ingrese un correo electrónico válido."
            )
            self.entries["email"].focus_set()
            return None

        return datos

    def _formatear_fila(self, cliente):
        return (
            getattr(cliente, "id_cliente", ""),
            getattr(cliente, "nombre", ""),
            getattr(cliente, "apellido", ""),
            getattr(cliente, "email", ""),
            getattr(cliente, "telefono", ""),
            getattr(cliente, "direccion_entrega", "")
        )

    def _cargar_en_formulario(self, datos):
        nombres = (
            "nombre",
            "apellido",
            "email",
            "telefono",
            "direccion_entrega"
        )

        # La primera columna de la tabla es el ID
        for indice, nombre in enumerate(nombres, start=1):
            entrada = self.entries[nombre]
            entrada.delete(0, "end")
            valor = datos[indice]
            entrada.insert(0, "" if valor is None else str(valor))