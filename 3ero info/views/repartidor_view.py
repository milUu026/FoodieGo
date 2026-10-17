
from tkinter import messagebox

from models.repartidor import Repartidor
from views.form_base import FormBase


class RepartidorView(FormBase):
    """Interfaz para gestionar los repartidores de FoodieGo."""

    titulo = "Gestión de Repartidores"

    columnas_tabla = (
        "ID",
        "Nombre",
        "Apellido",
        "Vehículo",
        "Placa",
        "Estado"
    )

    ancho_columnas = (50, 130, 130, 120, 100, 120)

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
            "nombre": "tipo_vehiculo",
            "etiqueta": "Tipo de vehículo",
            "tipo": "combobox",
            "valores": ["Moto", "Bicicleta", "Auto"]
        },
        {
            "nombre": "placa",
            "etiqueta": "Placa"
        },
        {
            "nombre": "estado",
            "etiqueta": "Estado",
            "tipo": "combobox",
            "valores": ["disponible", "en_ruta", "desconectado"]
        }
    )

    def __init__(self, parent):
        super().__init__(parent, Repartidor)

    def _obtener_datos_formulario(self):
        datos = {}

        for campo in self.campos_formulario:
            nombre = campo["nombre"]
            datos[nombre] = self.entries[nombre].get().strip()

        if not datos["nombre"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese el nombre del repartidor."
            )
            self.entries["nombre"].focus_set()
            return None

        if not datos["apellido"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese el apellido del repartidor."
            )
            self.entries["apellido"].focus_set()
            return None

        if not datos["estado"]:
            datos["estado"] = "disponible"

        # Permite dejar la placa vacía sin guardar una cadena vacía.
        if not datos["placa"]:
            datos["placa"] = None

        return datos

    def _formatear_fila(self, repartidor):
        return (
            getattr(repartidor, "id_repartidor", ""),
            getattr(repartidor, "nombre", ""),
            getattr(repartidor, "apellido", ""),
            getattr(repartidor, "tipo_vehiculo", ""),
            getattr(repartidor, "placa", "") or "",
            getattr(repartidor, "estado", "disponible")
        )

    def _cargar_en_formulario(self, datos):
        nombres = (
            "nombre",
            "apellido",
            "tipo_vehiculo",
            "placa",
            "estado"
        )

        for indice, nombre in enumerate(nombres, start=1):
            entrada = self.entries[nombre]
            entrada.delete(0, "end")
            valor = datos[indice]
            entrada.insert(0, "" if valor is None else str(valor))
