from src.models.database import Database
from datetime import datetime

class SolicitudPrestamo:
    def __init__(self, id=None, usuario_id=None, inventario_id=None, 
                 cantidad_solicitada=None, estado='pendiente', 
                 fecha_solicitud=None, fecha_respuesta=None, 
                 admin_id=None, comentario=None):
        self.id = id
        self.usuario_id = usuario_id
        self.inventario_id = inventario_id
        self.cantidad_solicitada = cantidad_solicitada
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud
        self.fecha_respuesta = fecha_respuesta
        self.admin_id = admin_id
        self.comentario = comentario
        self.db = Database()
        
        # Campos adicionales de JOINs
        self.usuario_nombre = None
        self.item_nombre = None
        self.laboratorio_nombre = None
        self.cantidad_disponible = 0
    
    def save(self):
        """Crea una nueva solicitud de préstamo"""
        query = """
        INSERT INTO solicitudes_prestamo 
        (usuario_id, inventario_id, cantidad_solicitada) 
        VALUES (%s, %s, %s)
        """
        params = (self.usuario_id, self.inventario_id, self.cantidad_solicitada)
        return self.db.execute_insert(query, params)
    
    @classmethod
    def get_all_pendientes(cls):
        """Obtiene todas las solicitudes pendientes"""
        db = Database()
        query = """
        SELECT s.*, u.username as usuario_nombre, 
               i.item_nombre, l.nombre as laboratorio_nombre,
               i.cantidad_disponible
        FROM solicitudes_prestamo s
        JOIN usuarios u ON s.usuario_id = u.id
        JOIN inventario i ON s.inventario_id = i.id
        JOIN laboratorios l ON i.laboratorio_id = l.id
        WHERE s.estado = 'pendiente'
        ORDER BY s.fecha_solicitud DESC
        """
        results = db.execute_query(query)
        return [cls._create_with_details(data) for data in results] if results else []
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las solicitudes"""
        db = Database()
        query = """
        SELECT s.*, u.username as usuario_nombre, 
               i.item_nombre, l.nombre as laboratorio_nombre,
               i.cantidad_disponible
        FROM solicitudes_prestamo s
        JOIN usuarios u ON s.usuario_id = u.id
        JOIN inventario i ON s.inventario_id = i.id
        JOIN laboratorios l ON i.laboratorio_id = l.id
        ORDER BY s.fecha_solicitud DESC
        """
        results = db.execute_query(query)
        return [cls._create_with_details(data) for data in results] if results else []
    
    @classmethod
    def get_by_usuario(cls, usuario_id):
        """Obtiene las solicitudes de un usuario"""
        db = Database()
        query = """
        SELECT s.*, u.username as usuario_nombre, 
               i.item_nombre, l.nombre as laboratorio_nombre,
               i.cantidad_disponible
        FROM solicitudes_prestamo s
        JOIN usuarios u ON s.usuario_id = u.id
        JOIN inventario i ON s.inventario_id = i.id
        JOIN laboratorios l ON i.laboratorio_id = l.id
        WHERE s.usuario_id = %s
        ORDER BY s.fecha_solicitud DESC
        """
        results = db.execute_query(query, (usuario_id,))
        return [cls._create_with_details(data) for data in results] if results else []
    
    def aprobar(self, admin_id):
        """Aprueba una solicitud"""
        query = """
        UPDATE solicitudes_prestamo 
        SET estado = 'aprobada', fecha_respuesta = NOW(), admin_id = %s 
        WHERE id = %s
        """
        return self.db.execute_insert(query, (admin_id, self.id))
    
    def rechazar(self, admin_id, comentario=None):
        """Rechaza una solicitud"""
        query = """
        UPDATE solicitudes_prestamo 
        SET estado = 'rechazada', fecha_respuesta = NOW(), 
            admin_id = %s, comentario = %s 
        WHERE id = %s
        """
        return self.db.execute_insert(query, (admin_id, comentario, self.id))
    
    @classmethod
    def _create_with_details(cls, data):
        """Crea objeto con datos de JOINs"""
        solicitud = cls(
            id=data['id'],
            usuario_id=data['usuario_id'],
            inventario_id=data['inventario_id'],
            cantidad_solicitada=data['cantidad_solicitada'],
            estado=data['estado'],
            fecha_solicitud=data['fecha_solicitud'],
            fecha_respuesta=data.get('fecha_respuesta'),
            admin_id=data.get('admin_id'),
            comentario=data.get('comentario')
        )
        solicitud.usuario_nombre = data.get('usuario_nombre')
        solicitud.item_nombre = data.get('item_nombre')
        solicitud.laboratorio_nombre = data.get('laboratorio_nombre')
        solicitud.cantidad_disponible = data.get('cantidad_disponible', 0)
        return solicitud
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'usuario_nombre': self.usuario_nombre,
            'inventario_id': self.inventario_id,
            'item_nombre': self.item_nombre,
            'laboratorio_nombre': self.laboratorio_nombre,
            'cantidad_solicitada': self.cantidad_solicitada,
            'cantidad_disponible': self.cantidad_disponible,
            'estado': self.estado,
            'fecha_solicitud': self.fecha_solicitud.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_solicitud else None,
            'fecha_respuesta': self.fecha_respuesta.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_respuesta else None,
            'comentario': self.comentario
        }