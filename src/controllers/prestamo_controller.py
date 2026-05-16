from src.models import Inventario, SolicitudPrestamo, PrestamoActivo

class PrestamoController:
    def __init__(self):
        self.usuario_actual = None
    
    def set_usuario(self, usuario_data):
        """Establece el usuario actual"""
        self.usuario_actual = usuario_data
    
    def solicitar_prestamo(self, inventario_id, cantidad):
        """
        Crea una solicitud de préstamo de inventario
        Retorna: (success, message)
        """
        try:
            if not self.usuario_actual:
                return False, "Debe iniciar sesión para solicitar préstamos"
            
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a 0"
            
            # Verificar que el item existe
            item = Inventario.get_by_id(inventario_id)
            if not item:
                return False, "Item no encontrado en el inventario"
            
            # Verificar disponibilidad
            if cantidad > item.cantidad_disponible:
                return False, f"No hay suficientes unidades. Disponibles: {item.cantidad_disponible}, Solicitado: {cantidad}"
            
            # Crear solicitud
            solicitud = SolicitudPrestamo(
                usuario_id=self.usuario_actual['id'],
                inventario_id=inventario_id,
                cantidad_solicitada=cantidad
            )
            
            result = solicitud.save()
            
            if result:
                return True, f"Solicitud de {cantidad} '{item.item_nombre}' enviada correctamente"
            else:
                return False, "Error al enviar la solicitud"
                
        except Exception as e:
            print(f"Error en solicitar_prestamo: {e}")
            return False, f"Error al procesar la solicitud: {str(e)}"
    
    def obtener_solicitudes_pendientes(self):
        """
        Obtiene todas las solicitudes pendientes (para admin)
        Retorna: (success, lista_solicitudes)
        """
        try:
            solicitudes = SolicitudPrestamo.get_all_pendientes()
            return True, [s.to_dict() for s in solicitudes]
        except Exception as e:
            print(f"Error en obtener_solicitudes_pendientes: {e}")
            return False, []
    
    def obtener_todas_solicitudes(self):
        """
        Obtiene todas las solicitudes (para historial)
        Retorna: (success, lista_solicitudes)
        """
        try:
            solicitudes = SolicitudPrestamo.get_all()
            return True, [s.to_dict() for s in solicitudes]
        except Exception as e:
            print(f"Error en obtener_todas_solicitudes: {e}")
            return False, []
    
    def obtener_mis_solicitudes(self):
        """
        Obtiene las solicitudes del usuario actual (maestro)
        Retorna: (success, lista_solicitudes)
        """
        try:
            if not self.usuario_actual:
                return False, "Debe iniciar sesión"
            
            solicitudes = SolicitudPrestamo.get_by_usuario(self.usuario_actual['id'])
            return True, [s.to_dict() for s in solicitudes]
        except Exception as e:
            print(f"Error en obtener_mis_solicitudes: {e}")
            return False, []
    
    def aprobar_solicitud(self, solicitud_id, admin_id):
        """
        Aprueba una solicitud y crea el préstamo activo
        Retorna: (success, message)
        """
        try:
            # Obtener la solicitud
            todas = SolicitudPrestamo.get_all()
            solicitud = next((s for s in todas if s.id == solicitud_id), None)
            
            if not solicitud:
                return False, "Solicitud no encontrada"
            
            if solicitud.estado != 'pendiente':
                return False, f"La solicitud ya fue {solicitud.estado}"
            
            # Verificar que aún haya disponibilidad
            item = Inventario.get_by_id(solicitud.inventario_id)
            if not item:
                return False, "El item ya no existe en el inventario"
            
            if solicitud.cantidad_solicitada > item.cantidad_disponible:
                return False, f"Ya no hay suficientes unidades. Disponibles: {item.cantidad_disponible}"
            
            # Aprobar la solicitud
            solicitud.aprobar(admin_id)
            
            # Crear el préstamo activo
            prestamo = PrestamoActivo(
                solicitud_id=solicitud_id,
                usuario_id=solicitud.usuario_id,
                inventario_id=solicitud.inventario_id,
                cantidad_prestada=solicitud.cantidad_solicitada
            )
            
            result = prestamo.save()
            
            if result:
                return True, f"Préstamo aprobado. Se prestaron {solicitud.cantidad_solicitada} '{item.item_nombre}'"
            else:
                return False, "Error al registrar el préstamo"
                
        except Exception as e:
            print(f"Error en aprobar_solicitud: {e}")
            return False, f"Error al aprobar: {str(e)}"
    
    def rechazar_solicitud(self, solicitud_id, admin_id, motivo=""):
        """
        Rechaza una solicitud de préstamo
        Retorna: (success, message)
        """
        try:
            todas = SolicitudPrestamo.get_all()
            solicitud = next((s for s in todas if s.id == solicitud_id), None)
            
            if not solicitud:
                return False, "Solicitud no encontrada"
            
            if solicitud.estado != 'pendiente':
                return False, f"La solicitud ya fue {solicitud.estado}"
            
            if not motivo:
                motivo = "Rechazada por el administrador"
            
            solicitud.rechazar(admin_id, motivo)
            return True, "Solicitud rechazada correctamente"
            
        except Exception as e:
            print(f"Error en rechazar_solicitud: {e}")
            return False, f"Error al rechazar: {str(e)}"
    
    def devolver_prestamo(self, prestamo_id):
        """
        Devuelve un préstamo activo (libera el inventario)
        Retorna: (success, message)
        """
        try:
            activos = PrestamoActivo.get_activos()
            prestamo = next((p for p in activos if p.id == prestamo_id), None)
            
            if not prestamo:
                return False, "Préstamo no encontrado"
            
            if prestamo.estado != 'prestado':
                return False, f"Este préstamo ya está {prestamo.estado}"
            
            result = prestamo.devolver()
            
            if result:
                item = Inventario.get_by_id(prestamo.inventario_id)
                item_nombre = item.item_nombre if item else "desconocido"
                return True, f"Préstamo devuelto. {prestamo.cantidad_prestada} '{item_nombre}' disponibles nuevamente"
            else:
                return False, "Error al procesar la devolución"
                
        except Exception as e:
            print(f"Error en devolver_prestamo: {e}")
            return False, f"Error al devolver: {str(e)}"
    
    def obtener_prestamos_activos(self):
        """
        Obtiene todos los préstamos activos (no devueltos)
        Retorna: (success, lista_prestamos)
        """
        try:
            prestamos = PrestamoActivo.get_activos()
            return True, [p.to_dict() for p in prestamos]
        except Exception as e:
            print(f"Error en obtener_prestamos_activos: {e}")
            return False, []
    
    def obtener_prestamos_historial(self):
        """
        Obtiene historial completo de préstamos
        Retorna: (success, lista_prestamos)
        """
        try:
            prestamos = PrestamoActivo.get_all()
            return True, [p.to_dict() for p in prestamos]
        except Exception as e:
            print(f"Error en obtener_prestamos_historial: {e}")
            return False, []
    
    def obtener_inventario_disponible(self):
        """
        Obtiene items del inventario con cantidad disponible > 0
        Retorna: (success, lista_items)
        """
        try:
            items = Inventario.get_all()
            disponibles = []
            for item in items:
                if item.cantidad_disponible > 0:
                    disponibles.append(item.to_dict())
            
            return True, disponibles
        except Exception as e:
            print(f"Error en obtener_inventario_disponible: {e}")
            return False, []
    
    def obtener_inventario_por_laboratorio(self, laboratorio_id):
        """
        Obtiene items disponibles de un laboratorio específico
        Retorna: (success, lista_items)
        """
        try:
            items = Inventario.get_by_laboratorio(laboratorio_id)
            disponibles = []
            for item in items:
                if item.cantidad_disponible > 0:
                    disponibles.append(item.to_dict())
            
            return True, disponibles
        except Exception as e:
            print(f"Error en obtener_inventario_por_laboratorio: {e}")
            return False, []
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas generales de préstamos
        Retorna: (success, dict_estadisticas)
        """
        try:
            solicitudes = SolicitudPrestamo.get_all()
            prestamos = PrestamoActivo.get_all()
            
            pendientes = len([s for s in solicitudes if s.estado == 'pendiente'])
            aprobadas = len([s for s in solicitudes if s.estado == 'aprobada'])
            rechazadas = len([s for s in solicitudes if s.estado == 'rechazada'])
            activos = len([p for p in prestamos if p.estado == 'prestado'])
            devueltos = len([p for p in prestamos if p.estado == 'devuelto'])
            
            stats = {
                'pendientes': pendientes,
                'aprobadas': aprobadas,
                'rechazadas': rechazadas,
                'activos': activos,
                'devueltos': devueltos,
                'total_solicitudes': len(solicitudes),
                'total_prestamos': len(prestamos)
            }
            
            return True, stats
        except Exception as e:
            print(f"Error en obtener_estadisticas: {e}")
            return False, {}