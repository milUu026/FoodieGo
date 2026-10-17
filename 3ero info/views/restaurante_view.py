from tkinter import messagebox

from models.restaurante import Restaurante
from views.form_base import FormBase


class RestauranteView(FormBase):
    """Interfaz para gestionar los restaurantes de FoodieGo."""

    titulo = "Gestión de Restaurantes"

    columnas_tabla = (
        "ID",
        "Nombre",
        "Tipo de cocina",
        "Dirección",
        "Teléfono",
        "Calificación"
    )

    ancho_columnas = (50, 150, 130, 200, 100, 90)

    campos_formulario = (
        {
            "nombre": "nombre",
            "etiqueta": "Nombre"
        },
        {
            "nombre": "tipo_cocina",
            "etiqueta": "Tipo de cocina"
        },
        {
            "nombre": "direccion",
            "etiqueta": "Dirección"
        },
        {
            "nombre": "telefono",
            "etiqueta": "Teléfono"
        },
        {
            "nombre": "calificacion_promedio",
            "etiqueta": "Calificación"
        }
    )

    def __init__(self, parent):
        super().__init__(parent, Restaurante)

    def _obtener_datos_formulario(self):
        datos = {}

        for campo in self.campos_formulario:
            nombre = campo["nombre"]
            datos[nombre] = self.entries[nombre].get().strip()

        if not datos["nombre"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese el nombre del restaurante."
            )
            self.entries["nombre"].focus_set()
            return None

        if not datos["direccion"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Ingrese la dirección del restaurante."
            )
            self.entries["direccion"].focus_set()
            return None

        try:
            calificacion = float(datos["calificacion_promedio"])
            if not 0 <= calificacion <= 5:
                raise ValueError
            datos["calificacion_promedio"] = calificacion
        except ValueError:
            messagebox.showwarning(
                "Calificación inválida",
                "Ingrese una calificación entre 0 y 5."
            )
            self.entries["calificacion_promedio"].focus_set()
            return None

        return datos

    def _formatear_fila(self, restaurante):
        return (
            getattr(restaurante, "id_restaurante", ""),
            getattr(restaurante, "nombre", ""),
            getattr(restaurante, "tipo_cocina", ""),
            getattr(restaurante, "direccion", ""),
            getattr(restaurante, "telefono", ""),
            getattr(restaurante, "calificacion_promedio", 0.0)
        )

    def _cargar_en_formulario(self, datos):
        nombres = (
            "nombre",
            "tipo_cocina",
            "direccion",
            "telefono",
            "calificacion_promedio"
        )

        for indice, nombre in enumerate(nombres, start=1):
            entrada = self.entries[nombre]
            entrada.delete(0, "end")
            valor = datos[indice]
            entrada.insert(0, "" if valor is None else str(valor))