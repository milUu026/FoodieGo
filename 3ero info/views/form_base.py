
import tkinter as tk
from tkinter import ttk, messagebox


class FormBase(tk.Toplevel):
    """Clase base para los formularios CRUD de FoodieGo."""

    titulo = "Formulario"
    columnas_tabla = ()
    ancho_columnas = ()
    campos_formulario = ()

    def __init__(self, parent, modelo):
        super().__init__(parent)

        self.modelo = modelo
        self.registro_seleccionado = None

        self.title(self.titulo)
        self.geometry("950x600")
        self.configure(bg="#ecf0f1")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._crear_formulario()
        self._crear_tabla()
        self._crear_botones()
        self.cargar_datos()

    def _crear_formulario(self):
        frame_form = tk.LabelFrame(
            self,
            text="Datos del Registro",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_form.pack(fill="x", padx=10, pady=5)

        self.entries = {}

        fila = 0
        col = 0

        for campo in self.campos_formulario:
            nombre = campo["nombre"]
            etiqueta = campo["etiqueta"]
            tipo = campo.get("tipo", "entry")

            tk.Label(
                frame_form,
                text=etiqueta + ":",
                font=("Arial", 9),
                bg="#ecf0f1"
            ).grid(
                row=fila,
                column=col,
                sticky="e",
                padx=5,
                pady=4
            )

            if tipo == "combobox":
                widget = ttk.Combobox(
                    frame_form,
                    width=27,
                    values=campo.get("valores", []),
                    state="readonly"
                )
            elif tipo == "text":
                widget = tk.Text(
                    frame_form,
                    width=30,
                    height=3,
                    font=("Arial", 9)
                )
            else:
                widget = tk.Entry(
                    frame_form,
                    width=30,
                    font=("Arial", 9)
                )

            widget.grid(
                row=fila,
                column=col + 1,
                padx=5,
                pady=4,
                sticky="w"
            )

            self.entries[nombre] = widget

            col += 2
            if col >= 4:
                col = 0
                fila += 1

    def _crear_tabla(self):
        frame_tabla = tk.LabelFrame(
            self,
            text="Registros guardados",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=self.columnas_tabla,
            show="headings",
            height=10
        )

        for i, columna in enumerate(self.columnas_tabla):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(
                columna,
                width=self.ancho_columnas[i],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self._al_seleccionar
        )

    def _crear_botones(self):
        frame_botones = tk.Frame(self, bg="#ecf0f1")
        frame_botones.pack(fill="x", padx=10, pady=10)

        botones = [
            ("Nuevo", self._limpiar_formulario, "#27ae60"),
            ("Guardar", self._guardar, "#2980b9"),
            ("Actualizar", self._actualizar, "#f39c12"),
            ("Eliminar", self._eliminar, "#c0392b"),
            ("Cerrar", self.destroy, "#7f8c8d")
        ]

        for texto, comando, color in botones:
            tk.Button(
                frame_botones,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Arial", 9, "bold"),
                width=12,
                relief="flat",
                cursor="hand2"
            ).pack(side="left", padx=4)

    def _al_seleccionar(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        fila = self.tabla.item(seleccion[0])["values"]
        self.registro_seleccionado = fila[0]
        self._cargar_en_formulario(fila)

    def _cargar_en_formulario(self, datos):
        """Las vistas hijas cargan aquí los datos seleccionados."""
        pass

    def _obtener_datos_formulario(self):
        """Las vistas hijas validan y devuelven los datos."""
        return {}

    def _formatear_fila(self, registro):
        """Las vistas hijas definen las columnas que mostrarán."""
        return ()

    def _limpiar_formulario(self):
        for widget in self.entries.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)

        self.registro_seleccionado = None

        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.selection_remove(*seleccion)

    def _guardar(self):
        try:
            datos = self._obtener_datos_formulario()
            if not datos:
                return

            registro = self.modelo(**datos)
            registro.save()

            messagebox.showinfo(
                "Éxito",
                "Registro guardado correctamente."
            )
            self._limpiar_formulario()
            self.cargar_datos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar el registro:\n{error}"
            )

    def _actualizar(self):
        if self.registro_seleccionado is None:
            messagebox.showwarning(
                "Atención",
                "Seleccione un registro de la tabla."
            )
            return

        try:
            datos = self._obtener_datos_formulario()
            if not datos:
                return

            registro = self.modelo.find_by_id(
                self.registro_seleccionado
            )

            if registro is None:
                messagebox.showwarning(
                    "Atención",
                    "El registro ya no existe."
                )
                self.cargar_datos()
                return

            registro.update(**datos)

            messagebox.showinfo(
                "Éxito",
                "Registro actualizado correctamente."
            )
            self._limpiar_formulario()
            self.cargar_datos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo actualizar:\n{error}"
            )

    def _eliminar(self):
        if self.registro_seleccionado is None:
            messagebox.showwarning(
                "Atención",
                "Seleccione un registro de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Desea eliminar el registro "
            f"#{self.registro_seleccionado}?"
        )

        if not confirmar:
            return

        try:
            registro = self.modelo.find_by_id(
                self.registro_seleccionado
            )

            if registro is not None:
                registro.delete()

            messagebox.showinfo(
                "Éxito",
                "Registro eliminado correctamente."
            )
            self._limpiar_formulario()
            self.cargar_datos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar:\n{error}"
            )

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        registros = self.modelo.all()

        for registro in registros:
            fila = self._formatear_fila(registro)
            self.tabla.insert("", "end", values=fila)
