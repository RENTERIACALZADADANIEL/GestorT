
from datetime import datetime, time, timedelta
from src.models.database import Database

class Reserva:
    def __init__(self, id=None, laboratorio_id=None, usuario_id=None, fecha=None, 
                 hora_inicio=None, hora_fin=None, estado='activa', created_at=None):
        self.id = id
        self.laboratorio_id = laboratorio_id
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.created_at = created_at
        self.db = Database()
    
    def save(self):
        """Crea una nueva reserva"""
        # Verificar disponibilidad antes de guardar
        if not self.verificar_disponibilidad():
            return False, "El horario seleccionado no está disponible"
        
        # Verificar que el laboratorio esté disponible
        if not self.verificar_laboratorio_disponible():
            return False, "El laboratorio no está disponible (en mantenimiento)"
        
        query = """
        INSERT INTO reservas (laboratorio_id, usuario_id, fecha, hora_inicio, hora_fin) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self.laboratorio_id,
            self.usuario_id,
            self.fecha,
            self.hora_inicio,
            self.hora_fin
        )
        result = self.db.execute_insert(query, params)
        return (True, result) if result else (False, "Error al crear la reserva")
    
    def verificar_disponibilidad(self):
        """Verifica si el horario está disponible para el laboratorio"""
        query = """
        SELECT COUNT(*) as count 
        FROM reservas 
        WHERE laboratorio_id = %s 
        AND fecha = %s 
        AND estado = 'activa'
        AND id != %s
        AND (
            (hora_inicio < %s AND hora_fin > %s)
            OR (hora_inicio >= %s AND hora_inicio < %s)
        )
        """
        params = (
            self.laboratorio_id,
            self.fecha,
            self.id or 0,
            self.hora_fin,
            self.hora_inicio,
            self.hora_inicio,
            self.hora_fin
        )
        result = self.db.execute_query(query, params)
        return result[0]['count'] == 0 if result else False
    
    def verificar_laboratorio_disponible(self):
        """Verifica que el laboratorio no esté en mantenimiento"""
        query = "SELECT estado FROM laboratorios WHERE id = %s"
        result = self.db.execute_query(query, (self.laboratorio_id,))
        return result and result[0]['estado'] == 'disponible'
    
    @classmethod
    def get_bloques_disponibles(cls, laboratorio_id, fecha):
        """Obtiene los bloques horarios disponibles para un laboratorio en una fecha"""
        db = Database()
        query = """
        SELECT bh.id, bh.hora_inicio, bh.hora_fin,
               CASE WHEN r.id IS NOT NULL THEN 'ocupado' ELSE 'disponible' END as estado
        FROM bloques_horario bh
        LEFT JOIN reservas r ON r.laboratorio_id = %s 
            AND r.fecha = %s 
            AND r.estado = 'activa'
            AND r.hora_inicio = bh.hora_inicio 
            AND r.hora_fin = bh.hora_fin
        WHERE bh.es_receso = 0
        ORDER BY bh.hora_inicio
        """
        params = (laboratorio_id, fecha)
        return db.execute_query(query, params)
    
    @classmethod
    def get_by_id(cls, reserva_id):
        """Obtiene una reserva por su ID"""
        db = Database()
        query = """
        SELECT r.*, l.nombre as laboratorio_nombre, u.username as usuario_nombre
        FROM reservas r
        JOIN laboratorios l ON r.laboratorio_id = l.id
        JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.id = %s
        """
        result = db.execute_query(query, (reserva_id,))
        if result:
            return cls._create_with_details(result[0])
        return None
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las reservas con detalles"""
        db = Database()
        query = """
        SELECT r.*, l.nombre as laboratorio_nombre, u.username as usuario_nombre
        FROM reservas r
        JOIN laboratorios l ON r.laboratorio_id = l.id
        JOIN usuarios u ON r.usuario_id = u.id
        ORDER BY r.fecha DESC, r.hora_inicio
        """
        results = db.execute_query(query)
        return [cls._create_with_details(data) for data in results] if results else []
    
    @classmethod
    def get_by_usuario(cls, usuario_id):
        """Obtiene las reservas de un usuario específico"""
        db = Database()
        query = """
        SELECT r.*, l.nombre as laboratorio_nombre, u.username as usuario_nombre
        FROM reservas r
        JOIN laboratorios l ON r.laboratorio_id = l.id
        JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.usuario_id = %s
        ORDER BY r.fecha DESC, r.hora_inicio
        """
        results = db.execute_query(query, (usuario_id,))
        return [cls._create_with_details(data) for data in results] if results else []
    
    @classmethod
    def get_by_laboratorio(cls, laboratorio_id):
        """Obtiene las reservas de un laboratorio específico"""
        db = Database()
        query = """
        SELECT r.*, l.nombre as laboratorio_nombre, u.username as usuario_nombre
        FROM reservas r
        JOIN laboratorios l ON r.laboratorio_id = l.id
        JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.laboratorio_id = %s
        ORDER BY r.fecha DESC, r.hora_inicio
        """
        results = db.execute_query(query, (laboratorio_id,))
        return [cls._create_with_details(data) for data in results] if results else []
    
    @classmethod
    def get_dashboard_admin(cls):
        """Obtiene todas las reservas para el dashboard del admin"""
        db = Database()
        query = """
        SELECT r.id, r.fecha, r.hora_inicio, r.hora_fin, r.estado,
               l.nombre as laboratorio_nombre, 
               u.username as usuario_nombre, u.rol as usuario_rol
        FROM reservas r
        JOIN laboratorios l ON r.laboratorio_id = l.id
        JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.estado = 'activa'
        ORDER BY r.fecha DESC, r.hora_inicio
        """
        return db.execute_query(query)
    
    def cancelar(self):
        """Cancela una reserva"""
        self.estado = 'cancelada'
        query = "UPDATE reservas SET estado = 'cancelada' WHERE id = %s"
        return self.db.execute_insert(query, (self.id,))
    
    def delete(self):
        """Elimina una reserva"""
        query = "DELETE FROM reservas WHERE id = %s"
        return self.db.execute_insert(query, (self.id,))
    
    @classmethod
    def _create_with_details(cls, data):
        """Crea un objeto Reserva con datos adicionales de JOINs"""
        reserva = cls(
            id=data['id'],
            laboratorio_id=data['laboratorio_id'],
            usuario_id=data['usuario_id'],
            fecha=data['fecha'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin'],
            estado=data['estado'],
            created_at=data['created_at']
        )
        reserva.laboratorio_nombre = data.get('laboratorio_nombre')
        reserva.usuario_nombre = data.get('usuario_nombre')
        return reserva
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        hora_inicio_str = str(self.hora_inicio) if self.hora_inicio else None
        hora_fin_str = str(self.hora_fin) if self.hora_fin else None
        
        return {
            'id': self.id,
            'laboratorio_id': self.laboratorio_id,
            'usuario_id': self.usuario_id,
            'fecha': str(self.fecha) if self.fecha else None,
            'hora_inicio': hora_inicio_str,
            'hora_fin': hora_fin_str,
            'estado': self.estado,
            'laboratorio_nombre': getattr(self, 'laboratorio_nombre', None),
            'usuario_nombre': getattr(self, 'usuario_nombre', None),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }