# from database.connection import DatabaseConnection
# from models.cliente import Cliente
# from models.restaurante import Restaurante
# from models.repartidor import Repartidor
# from models.pedido import Pedido
#
# print("=" * 60)
# print("🛵 FOODIEGO - SISTEMA DE PEDIDOS")
# print("=" * 60)
#
# # Inicializar base de datos
# DatabaseConnection.initialize_tables()
#
# # ==================== CREAR DATOS ====================
# print("\n📝 CREANDO DATOS DE PRUEBA...\n")
#
# # Crear clientes
# cliente1 = Cliente(
#     nombre="María",
#     apellido="Rodríguez",
#     email="maria@email.com",
#     telefono="555-1111",
#     direccion_entrega="Av. Principal 123"
# )
# cliente1.save()
#
# cliente2 = Cliente(
#     nombre="Carlos",
#     apellido="López",
#     email="carlos@email.com",
#     telefono="555-2222",
#     direccion_entrega="Calle 456"
# )
# cliente2.save()
#
# # Crear restaurantes
# restaurante1 = Restaurante(
#     nombre="Pizza Italia",
#     tipo_cocina="Italiana",
#     direccion="Calle Roma 789",
#     telefono="555-3333",
#     calificacion_promedio=4.5
# )
# restaurante1.save()
#
# restaurante2 = Restaurante(
#     nombre="Tacos México",
#     tipo_cocina="Mexicana",
#     direccion="Av. México 321",
#     telefono="555-4444",
#     calificacion_promedio=4.8
# )
# restaurante2.save()
#
# # Crear repartidores
# repartidor1 = Repartidor(
#     nombre="Juan",
#     apellido="Pérez",
#     tipo_vehiculo="Moto",
#     placa="ABC-123",
#     estado="disponible"
# )
# repartidor1.save()
#
# repartidor2 = Repartidor(
#     nombre="Ana",
#     apellido="García",
#     tipo_vehiculo="Bicicleta",
#     placa="XYZ-789",
#     estado="disponible"
# )
# repartidor2.save()
#
# # Crear pedidos
# pedido1 = Pedido(
#     id_cliente=cliente1.id_cliente,
#     id_restaurante=restaurante1.id_restaurante,
#     id_repartidor=None,  # Sin asignar inicialmente
#     estado="pendiente",
#     total=25.50
# )
# pedido1.save()
#
# pedido2 = Pedido(
#     id_cliente=cliente2.id_cliente,
#     id_restaurante=restaurante2.id_restaurante,
#     id_repartidor=None,
#     estado="pendiente",
#     total=18.75
# )
# pedido2.save()
#
# # ==================== LEER DATOS ====================
# print("\n" + "=" * 60)
# print("📊 CONSULTANDO DATOS...\n")
#
# # Mostrar todos los clientes
# print("--- CLIENTES ---")
# for c in Cliente.all():
#     print(f"ID {c.id_cliente}: {c.nombre} {c.apellido} ({c.email})")
#
# # Mostrar todos los restaurantes
# print("\n--- RESTAURANTES ---")
# for r in Restaurante.all():
#     print(f"ID {r.id_restaurante}: {r.nombre} - {r.tipo_cocina} ⭐{r.calificacion_promedio}")
#
# # Mostrar todos los repartidores
# print("\n--- REPARTIDORES ---")
# for rep in Repartidor.all():
#     print(f"ID {rep.id_repartidor}: {rep.nombre} {rep.apellido} - {rep.tipo_vehiculo} [{rep.estado}]")
#
# # Mostrar detalles de pedidos
# print("\n--- PEDIDOS ---")
# for p in Pedido.all():
#     p.detalles_pedido()
#
# # ==================== RELACIONES ====================
# print("\n" + "=" * 60)
# print("🔗 PROBANDO RELACIONES...\n")
#
# # Obtener pedidos de un restaurante
# print(f"📦 Pedidos de '{restaurante1.nombre}':")
# pedidos_rest1 = restaurante1.get_pedidos()
# for p in pedidos_rest1:
#     print(f"  - Pedido #{p.id_pedido} - Total: ${p.total}")
#
# # Asignar repartidor a un pedido
# print(f"\n🚴 Asignando repartidor al pedido #{pedido1.id_pedido}...")
# repartidor1.asignar_pedido(pedido1.id_pedido)
#
# # Ver detalles actualizados
# pedido_actualizado = Pedido.find_by_id(pedido1.id_pedido)
# pedido_actualizado.detalles_pedido()
#
# # Ver pedidos asignados a un repartidor
# print(f"\n📦 Pedidos asignados a {repartidor1.nombre}:")
# pedidos_rep1 = repartidor1.get_pedidos_asignados()
# for p in pedidos_rep1:
#     print(f"  - Pedido #{p.id_pedido} - Estado: {p.estado}")
#
# # ==================== RESUMEN FINAL ====================
# print("\n" + "=" * 60)
# print("✅ SISTEMA COMPLETO FUNCIONANDO")
# print("=" * 60)
# print(f"Total clientes: {len(Cliente.all())}")
# print(f"Total restaurantes: {len(Restaurante.all())}")
# print(f"Total repartidores: {len(Repartidor.all())}")
# print(f"Total pedidos: {len(Pedido.all())}")
import tkinter as tk
from views.main_window import MainWindow


def main():
    # Crear la ventana raíz
    root = tk.Tk()

    # Crear la aplicación
    app = MainWindow(root)

    # Iniciar el loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()