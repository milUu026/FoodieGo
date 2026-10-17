
import tkinter as tk
from tkinter import messagebox

from database.connection import DatabaseConnection
from views.cliente_view import ClienteView
from views.restaurante_view import RestauranteView
from views.repartidor_view import RepartidorView
from views.pedido_view import PedidoView


class MainWindow:
    """Ventana principal de la aplicación FoodieGo."""

    def __init__(self, root):
        self.root = root
        self.root.title("FoodieGo - Sistema de Gestión")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Inicializar la base de datos
        DatabaseConnection.initialize_tables()

        self._crear_menu()
        self._crear_pantalla_inicio()

    def _crear_menu(self):
        """Crea la barra de menú superior."""
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        # Menú Archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(
            label="Revisar base de datos",
            command=self._reiniciar_bd
        )
        menu_archivo.add_separator()
        menu_archivo.add_command(
            label="Salir",
            command=self.root.quit
        )
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú Gestión
        menu_gestion = tk.Menu(barra_menu, tearoff=0)
        menu_gestion.add_command(
            label="Clientes",
            command=self._abrir_clientes
        )
        menu_gestion.add_command(
            label="Restaurantes",
            command=self._abrir_restaurantes
        )
        menu_gestion.add_command(
            label="Repartidores",
            command=self._abrir_repartidores
        )
        menu_gestion.add_command(
            label="Pedidos",
            command=self._abrir_pedidos
        )
        barra_menu.add_cascade(label="Gestión", menu=menu_gestion)

        # Menú Ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(
            label="Acerca de",
            command=self._acerca_de
        )
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

    def _crear_pantalla_inicio(self):
        """Crea la pantalla de bienvenida."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        frame_inicio = tk.Frame(self.root, bg="#f0f0f0")
        frame_inicio.pack(expand=True, fill="both")

        tk.Label(
            frame_inicio,
            text="FoodieGo",
            font=("Arial", 32, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=25)

        tk.Label(
            frame_inicio,
            text="Sistema de Gestión de Pedidos",
            font=("Arial", 16),
            bg="#f0f0f0",
            fg="#7f8c8d"
        ).pack(pady=10)

        tk.Label(
            frame_inicio,
            text="Seleccione una opción del menú Gestión para comenzar.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#555555"
        ).pack(pady=30)

    def _abrir_clientes(self):
        ClienteView(self.root)

    def _abrir_restaurantes(self):
        RestauranteView(self.root)

    def _abrir_repartidores(self):
        RepartidorView(self.root)

    def _abrir_pedidos(self):
        PedidoView(self.root)

    def _reiniciar_bd(self):
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea comprobar e inicializar las tablas?"
        )
        if respuesta:
            try:
                DatabaseConnection.initialize_tables()
                messagebox.showinfo(
                    "Base de datos",
                    "Se ejecutó la inicialización de las tablas."
                )
            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo inicializar la base de datos:\n{error}"
                )

    def _acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "FoodieGo v1.0\n\n"
            "Sistema de gestión de pedidos\n"
            "Desarrollado con Python, Tkinter y ORM."
        )
