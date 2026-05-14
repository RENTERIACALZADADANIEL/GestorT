from src.models import Inventario, SolicitudPrestamo, PrestamoActivo

class PrestamoController:
    def __init__(self):
        self.usuario_actual = None
    
    def set_usuario(self, usuario_data):
        self.usuario_actual = usuario_data
    
    def solicitar_prestamo(self, inventario_id, cantidad):
        """Crea una solicitud de préstamo"""
        try:
            if not self.usuario_actual:
                return False, "Debe iniciar sesión"
            
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a 0"
            
            # Verificar inventario
            item = Inventario.get_by_id(inventario_id)
            if not item:
                return False, "Item no encontrado"
            
            if cantidad > item.cantidad_disponible:
                return False, f"Solo hay {item.cantidad_disponible} disponibles"
            
            # Crear solicitud
            solicitud = SolicitudPrestamo(
                usuario_id=self.usuario_actual['id'],
                inventario_id=inventario_id,
                cantidad_solicitada=cantidad
            )
            
            result = solicitud.save()
            if result:
                return True, "Solicitud enviada correctamente"
            return False, "Error al enviar solicitud"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_solicitudes_pendientes(self):
        """Obtiene solicitudes pendientes (para admin)"""
        try:
            solicitudes = SolicitudPrestamo.get_all_pendientes()
            return True, [s.to_dict() for s in solicitudes]
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_mis_solicitudes(self):
        """Obtiene solicitudes del usuario actual"""
        try:
            if not self.usuario_actual:
                return False, "Debe iniciar sesión"
            
            solicitudes = SolicitudPrestamo.get_by_usuario(self.usuario_actual['id'])
            return True, [s.to_dict() for s in solicitudes]
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def aprobar_solicitud(self, solicitud_id, admin_id):
        """Aprueba una solicitud y crea préstamo activo"""
        try:
            solicitud = SolicitudPrestamo.get_all()
            solicitud = next((s for s in solicitud if s.id == solicitud_id), None)
            
            if not solicitud:
                return False, "Solicitud no encontrada"
            
            if solicitud.estado != 'pendiente':
                return False, "La solicitud ya fue procesada"
            
            # Aprobar solicitud
            solicitud.aprobar(admin_id)
            
            # Crear préstamo activo
            prestamo = PrestamoActivo(
                solicitud_id=solicitud_id,
                usuario_id=solicitud.usuario_id,
                inventario_id=solicitud.inventario_id,
                cantidad_prestada=solicitud.cantidad_solicitada
            )
            
            result = prestamo.save()
            if result:
                return True, "Préstamo aprobado exitosamente"
            return False, "Error al crear préstamo"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def rechazar_solicitud(self, solicitud_id, admin_id, motivo=""):
        """Rechaza una solicitud"""
        try:
            solicitudes = SolicitudPrestamo.get_all()
            solicitud = next((s for s in solicitudes if s.id == solicitud_id), None)
            
            if not solicitud:
                return False, "Solicitud no encontrada"
            
            solicitud.rechazar(admin_id, motivo)
            return True, "Solicitud rechazada"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def devolver_prestamo(self, prestamo_id):
        """Devuelve un préstamo activo"""
        try:
            prestamos = PrestamoActivo.get_activos()
            prestamo = next((p for p in prestamos if p.id == prestamo_id), None)
            
            if not prestamo:
                return False, "Préstamo no encontrado"
            
            if prestamo.estado != 'prestado':
                return False, "Este préstamo ya fue devuelto"
            
            result = prestamo.devolver()
            if result:
                return True, "Préstamo devuelto exitosamente"
            return False, "Error al devolver préstamo"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_prestamos_activos(self):
        """Obtiene préstamos activos (no devueltos)"""
        try:
            prestamos = PrestamoActivo.get_activos()
            return True, [p.to_dict() for p in prestamos]
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_inventario_disponible(self):
        """Obtiene items con cantidad disponible > 0"""
        try:
            items = Inventario.get_all()
            disponibles = [item.to_dict() for item in items if item.cantidad_disponible > 0]
            return True, disponibles
        except Exception as e:
            return False, f"Error: {str(e)}"