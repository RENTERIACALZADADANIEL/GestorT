from models import Laboratorio, Reserva, Usuario, Inventario
from datetime import datetime, date

class AdminController:
    def __init__(self):
        self.admin_actual = None
    
    def set_admin(self, admin_data):
        """Establece el administrador actual"""
        self.admin_actual = admin_data
    
    # ===== GESTIÓN DE LABORATORIOS =====
    def crear_laboratorio(self, nombre, estado='disponible'):
        """
        Crea un nuevo laboratorio
        Retorna: (success, message)
        """
        try:
            # Validar campos
            if not nombre:
                return False, "El nombre del laboratorio es obligatorio"
            
            if estado not in ['disponible', 'mantenimiento']:
                return False, "Estado no válido"
            
            # Crear laboratorio
            nuevo_lab = Laboratorio(nombre=nombre, estado=estado)
            result = nuevo_lab.save()
            
            if result:
                return True, f"Laboratorio '{nombre}' creado exitosamente"
            else:
                return False, "Error al crear el laboratorio"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_laboratorios(self):
        """Obtiene todos los laboratorios"""
        try:
            laboratorios = Laboratorio.get_all()
            return True, [lab.to_dict() for lab in laboratorios]
        except Exception as e:
            return False, f"Error al obtener laboratorios: {str(e)}"
    
    def obtener_laboratorio_por_id(self, lab_id):
        """Obtiene un laboratorio específico"""
        try:
            laboratorio = Laboratorio.get_by_id(lab_id)
            if laboratorio:
                return True, laboratorio.to_dict()
            return False, "Laboratorio no encontrado"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def actualizar_laboratorio(self, lab_id, nombre, estado):
        """
        Actualiza un laboratorio existente
        Retorna: (success, message)
        """
        try:
            # Validar campos
            if not nombre:
                return False, "El nombre es obligatorio"
            
            if estado not in ['disponible', 'mantenimiento']:
                return False, "Estado no válido"
            
            laboratorio = Laboratorio.get_by_id(lab_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            laboratorio.nombre = nombre
            laboratorio.estado = estado
            
            result = laboratorio.update()
            if result:
                return True, "Laboratorio actualizado exitosamente"
            else:
                return False, "Error al actualizar laboratorio"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cambiar_estado_laboratorio(self, lab_id, nuevo_estado):
        """
        Cambia el estado de un laboratorio (disponible/mantenimiento)
        Retorna: (success, message)
        """
        try:
            if nuevo_estado not in ['disponible', 'mantenimiento']:
                return False, "Estado no válido"
            
            laboratorio = Laboratorio.get_by_id(lab_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            result = laboratorio.cambiar_estado(nuevo_estado)
            if result:
                estado_str = "disponible" if nuevo_estado == 'disponible' else "en mantenimiento"
                return True, f"Laboratorio marcado como {estado_str}"
            else:
                return False, "Error al cambiar estado"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_laboratorio(self, lab_id):
        """
        Elimina un laboratorio
        Retorna: (success, message)
        """
        try:
            laboratorio = Laboratorio.get_by_id(lab_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            result = laboratorio.delete()
            if result:
                return True, f"Laboratorio '{laboratorio.nombre}' eliminado exitosamente"
            else:
                return False, "Error al eliminar laboratorio"
                
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    # ===== DASHBOARD ADMIN =====
    def obtener_dashboard(self):
        """
        Obtiene todas las reservas activas para el dashboard
        Retorna: (success, data)
        """
        try:
            reservas = Reserva.get_dashboard_admin()
            
            # Formatear datos para el dashboard
            dashboard_data = []
            if reservas:
                for reserva in reservas:
                    dashboard_data.append({
                        'id': reserva['id'],
                        'fecha': str(reserva['fecha']),
                        'hora_inicio': str(reserva['hora_inicio']),
                        'hora_fin': str(reserva['hora_fin']),
                        'laboratorio': reserva['laboratorio_nombre'],
                        'usuario': reserva['usuario_nombre'],
                        'rol': reserva['usuario_rol'],
                        'estado': reserva['estado']
                    })
            
            return True, dashboard_data
            
        except Exception as e:
            return False, f"Error al cargar dashboard: {str(e)}"
    
    # ===== GESTIÓN DE RESERVAS (Admin) =====
    def cancelar_reserva(self, reserva_id):
        """
        Cancela una reserva existente
        Retorna: (success, message)
        """
        try:
            reserva = Reserva.get_by_id(reserva_id)
            if not reserva:
                return False, "Reserva no encontrada"
            
            if reserva.estado == 'cancelada':
                return False, "La reserva ya está cancelada"
            
            result = reserva.cancelar()
            if result:
                return True, "Reserva cancelada exitosamente"
            else:
                return False, "Error al cancelar reserva"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_reserva(self, reserva_id):
        """
        Elimina una reserva
        Retorna: (success, message)
        """
        try:
            reserva = Reserva.get_by_id(reserva_id)
            if not reserva:
                return False, "Reserva no encontrada"
            
            result = reserva.delete()
            if result:
                return True, "Reserva eliminada exitosamente"
            else:
                return False, "Error al eliminar reserva"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_todas_reservas(self):
        """Obtiene todas las reservas del sistema"""
        try:
            reservas = Reserva.get_all()
            return True, [reserva.to_dict() for reserva in reservas]
        except Exception as e:
            return False, f"Error al obtener reservas: {str(e)}"
    
    # ===== GESTIÓN DE INVENTARIO =====
    def agregar_item_inventario(self, laboratorio_id, item_nombre, cantidad):
        """
        Agrega un item al inventario
        Retorna: (success, message)
        """
        try:
            # Validar campos
            if not laboratorio_id or not item_nombre or cantidad is None:
                return False, "Todos los campos son obligatorios"
            
            if cantidad < 0:
                return False, "La cantidad no puede ser negativa"
            
            # Verificar que el laboratorio existe
            laboratorio = Laboratorio.get_by_id(laboratorio_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            # Agregar item
            nuevo_item = Inventario(
                laboratorio_id=laboratorio_id,
                item_nombre=item_nombre,
                cantidad_total=cantidad
            )
            
            result = nuevo_item.save()
            if result:
                return True, f"Item '{item_nombre}' agregado al inventario"
            else:
                return False, "Error al agregar item"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_inventario(self):
        """Obtiene todo el inventario"""
        try:
            items = Inventario.get_all()
            return True, [item.to_dict() for item in items]
        except Exception as e:
            return False, f"Error al obtener inventario: {str(e)}"
    
    def obtener_inventario_laboratorio(self, laboratorio_id):
        """Obtiene el inventario de un laboratorio específico"""
        try:
            items = Inventario.get_by_laboratorio(laboratorio_id)
            return True, [item.to_dict() for item in items]
        except Exception as e:
            return False, f"Error al obtener inventario: {str(e)}"
    
    def actualizar_cantidad_inventario(self, item_id, nueva_cantidad):
        """
        Actualiza la cantidad de un item
        Retorna: (success, message)
        """
        try:
            if nueva_cantidad < 0:
                return False, "La cantidad no puede ser negativa"
            
            item = Inventario.get_by_id(item_id)
            if not item:
                return False, "Item no encontrado"
            
            result = item.actualizar_cantidad(nueva_cantidad)
            if result:
                return True, "Cantidad actualizada exitosamente"
            else:
                return False, "Error al actualizar cantidad"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_item_inventario(self, item_id):
        """
        Elimina un item del inventario
        Retorna: (success, message)
        """
        try:
            item = Inventario.get_by_id(item_id)
            if not item:
                return False, "Item no encontrado"
            
            result = item.delete()
            if result:
                return True, f"Item '{item.item_nombre}' eliminado del inventario"
            else:
                return False, "Error al eliminar item"
                
        except Exception as e:
            return False, f"Error: {str(e)}"