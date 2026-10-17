
import tkinter as tk
from tkinter import ttk, messagebox

from models.cliente import Cliente
from models.restaurante import Restaurante
from models.repartidor import Repartidor
from models.pedido import Pedido


class PedidoView(tk.Toplevel):
    """Interfaz para gestionar los pedidos de FoodieGo."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Gestión de Pedidos")
        self.geometry("950x580")
        self.configure(bg="#ecf0f1")
        self.transient(parent)
        self.grab_set()

        self.id_seleccionado = None
        self.clientes = {}
        self.restaurantes = {}
        self.repartidores = {}

        self._crear_formulario()
        self._crear_tabla()
        self._crear_botones()
        self._cargar_opciones()
        self.cargar_pedidos()

    def _crear_formulario(self):
        frame = tk.LabelFrame(
            self,
            text="Datos del pedido",
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            frame,
            text="Cliente:",
            bg="#ecf0f1"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.combo_cliente = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            frame,
            text="Restaurante:",
            bg="#ecf0f1"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.combo_restaurante = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )
        self.combo_restaurante.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            frame,
            text="Repartidor:",
            bg="#ecf0f1"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.combo_repartidor = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )
        self.combo_repartidor.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(
            frame,
            text="Estado:",
            bg="#ecf0f1"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.combo_estado = ttk.Combobox(
            frame,
            width=22,
            state="readonly",
            values=[
                "pendiente",
                "en_preparacion",
                "en_camino",
                "entregado",
                "cancelado"
            ]
        )
        self.combo_estado.grid(row=0, column=3, padx=5, pady=5)
        self.combo_estado.set("pendiente")

        tk.Label(
            frame,
            text="Total:",
            bg="#ecf0f1"
        ).grid(row=1, column=2, padx=5, pady=5, sticky="e")

        self.entry_total = tk.Entry(frame, width=25)
        self.entry_total.grid(row=1, column=3, padx=5, pady=5)

    def _crear_tabla(self):
        frame = tk.LabelFrame(
            self,
            text="Pedidos registrados",
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = (
            "ID",
            "Cliente",
            "Restaurante",
            "Repartidor",
            "Estado",
            "Total"
        )

        self.tabla = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings"
        )

        anchos = (50, 150, 150, 150, 120, 90)

        for columna, ancho in zip(columnas, anchos):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(
                columna,
                width=ancho,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self._seleccionar_pedido
        )

    def _crear_botones(self):
        frame = tk.Frame(self, bg="#ecf0f1")
        frame.pack(fill="x", padx=10, pady=10)

        botones = [
            ("Nuevo", self._limpiar),
            ("Guardar", self._guardar),
            ("Actualizar", self._actualizar),
            ("Eliminar", self._eliminar),
            ("Cerrar", self.destroy)
        ]

        for texto, comando in botones:
            tk.Button(
                frame,
                text=texto,
                command=comando,
                width=13,
                cursor="hand2"
            ).pack(side="left", padx=5)

    def _cargar_opciones(self):
        lista_clientes = Cliente.all()
        lista_restaurantes = Restaurante.all()
        lista_repartidores = Repartidor.all()

        self.clientes = {
            f"{c.id_cliente} - {c.nombre} {c.apellido}": c.id_cliente
            for c in lista_clientes
        }

        self.restaurantes = {
            f"{r.id_restaurante} - {r.nombre}": r.id_restaurante
            for r in lista_restaurantes
        }

        self.repartidores = {
            f"{r.id_repartidor} - {r.nombre} {r.apellido}": r.id_repartidor
            for r in lista_repartidores
        }

        self.combo_cliente["values"] = list(self.clientes.keys())
        self.combo_restaurante["values"] = list(self.restaurantes.keys())
        self.combo_repartidor["values"] = (
            ["Sin asignar"] + list(self.repartidores.keys())
        )

        self.combo_repartidor.set("Sin asignar")

    def _obtener_datos(self):
        cliente_texto = self.combo_cliente.get()
        restaurante_texto = self.combo_restaurante.get()
        repartidor_texto = self.combo_repartidor.get()
        estado = self.combo_estado.get()
        total_texto = self.entry_total.get().strip()

        if cliente_texto not in self.clientes:
            messagebox.showwarning(
                "Dato obligatorio",
                "Seleccione un cliente."
            )
            return None

        if restaurante_texto not in self.restaurantes:
            messagebox.showwarning(
                "Dato obligatorio",
                "Seleccione un restaurante."
            )
            return None

        if not estado:
            messagebox.showwarning(
                "Dato obligatorio",
                "Seleccione el estado del pedido."
            )
            return None

        try:
            total = float(total_texto)
            if total < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Total inválido",
                "Ingrese un total numérico igual o mayor que cero."
            )
            self.entry_total.focus_set()
            return None

        id_repartidor = self.repartidores.get(repartidor_texto)

        return {
            "id_cliente": self.clientes[cliente_texto],
            "id_restaurante": self.restaurantes[restaurante_texto],
            "id_repartidor": id_repartidor,
            "estado": estado,
            "total": total
        }

    def _guardar(self):
        try:
            datos = self._obtener_datos()
            if datos is None:
                return

            pedido = Pedido(**datos)
            pedido.save()

            messagebox.showinfo(
                "Éxito",
                "Pedido guardado correctamente."
            )

            self._limpiar()
            self.cargar_pedidos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar el pedido:\n{error}"
            )

    def _actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Atención",
                "Seleccione un pedido de la tabla."
            )
            return

        try:
            datos = self._obtener_datos()
            if datos is None:
                return

            pedido = Pedido.find_by_id(self.id_seleccionado)

            if pedido is None:
                messagebox.showwarning(
                    "Atención",
                    "No se encontró el pedido seleccionado."
                )
                self.cargar_pedidos()
                return

            pedido.update(**datos)

            messagebox.showinfo(
                "Éxito",
                "Pedido actualizado correctamente."
            )

            self._limpiar()
            self.cargar_pedidos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el pedido:\n{error}"
            )

    def _eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Atención",
                "Seleccione un pedido de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar el pedido seleccionado?"
        )

        if not confirmar:
            return

        try:
            pedido = Pedido.find_by_id(self.id_seleccionado)

            if pedido is not None:
                pedido.delete()

            messagebox.showinfo(
                "Éxito",
                "Pedido eliminado correctamente."
            )

            self._limpiar()
            self.cargar_pedidos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el pedido:\n{error}"
            )

    def cargar_pedidos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for pedido in Pedido.all():
            cliente = pedido.get_cliente()
            restaurante = pedido.get_restaurante()
            repartidor = pedido.get_repartidor()

            nombre_cliente = (
                f"{cliente.nombre} {cliente.apellido}"
                if cliente else "No encontrado"
            )

            nombre_restaurante = (
                restaurante.nombre
                if restaurante else "No encontrado"
            )

            nombre_repartidor = (
                f"{repartidor.nombre} {repartidor.apellido}"
                if repartidor else "Sin asignar"
            )

            self.tabla.insert(
                "",
                "end",
                values=(
                    pedido.id_pedido,
                    nombre_cliente,
                    nombre_restaurante,
                    nombre_repartidor,
                    pedido.estado,
                    pedido.total
                )
            )

    def _seleccionar_pedido(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        fila = self.tabla.item(seleccion[0])["values"]
        self.id_seleccionado = fila[0]

        pedido = Pedido.find_by_id(self.id_seleccionado)
        if pedido is None:
            return

        self._cargar_opciones()

        cliente = Cliente.find_by_id(pedido.id_cliente)
        restaurante = Restaurante.find_by_id(pedido.id_restaurante)
        repartidor = (
            Repartidor.find_by_id(pedido.id_repartidor)
            if pedido.id_repartidor is not None
            else None
        )

        if cliente:
            clave = f"{cliente.id_cliente} - {cliente.nombre} {cliente.apellido}"
            self.combo_cliente.set(clave)

        if restaurante:
            clave = f"{restaurante.id_restaurante} - {restaurante.nombre}"
            self.combo_restaurante.set(clave)

        if repartidor:
            clave = f"{repartidor.id_repartidor} - {repartidor.nombre} {repartidor.apellido}"
            self.combo_repartidor.set(clave)
        else:
            self.combo_repartidor.set("Sin asignar")

        self.combo_estado.set(pedido.estado)
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, str(pedido.total))

    def _limpiar(self):
        self.id_seleccionado = None
        self.combo_cliente.set("")
        self.combo_restaurante.set("")
        self.combo_repartidor.set("Sin asignar")
        self.combo_estado.set("pendiente")
        self.entry_total.delete(0, tk.END)

        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.selection_remove(*seleccion)
