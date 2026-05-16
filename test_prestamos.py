import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.controllers.prestamo_controller import PrestamoController

pc = PrestamoController()
pc.set_usuario({'id': 3, 'username': 'maestro1', 'rol': 'maestro'})

# Ver items disponibles
success, items = pc.obtener_inventario_disponible()
print('Success:', success)
print('Type of items:', type(items))

if success and items:
    print('Total items:', len(items))
    for item in items:
        print(f"  ID:{item['id']}, Lab ID:{item['laboratorio_id']}, Lab:{item['laboratorio_nombre']}, Item:{item['item_nombre']}, Disp:{item['cantidad_disponible']}")
elif not success:
    print('Error:', items)
else:
    print('No hay items disponibles')