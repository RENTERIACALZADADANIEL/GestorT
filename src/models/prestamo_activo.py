from src.models.database import Database
from datetime import datetime

class PrestamoActivo:
    def __init__(self, id=None, solicitud_id=None, usuario_id=None, 
                 inventario_id=None, cantidad_prestada=None, 
                 fecha_prestamo=None, fecha_devolucion=None, estado='prestado'):
        self.id = id
        self.solicitud_id = solicitud_id
        self.usuario_id = usuario_id
        self.inventario_id = inventario_id
        self.cantidad_prestada = cantidad_prestada
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado
        self.db = Database()
        
        # Campos JOIN
        self.usuario_nombre = None
        self.item_nombre = None
        self.laboratorio_nombre = None
    
    def save(self):
        """Registra un préstamo activo y actualiza inventario"""
        # Iniciar transacción
        connection = self.db.connect()
        cursor = connection.cursor()
        
        try:
            # Insertar préstamo
            query = """
            INSERT INTO prestamos_activos 
            (solicitud_id, usuario_id, inventario_id, cantidad_prestada) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.solicitud_id, self.usuario_id, 
                                   self.inventario_id, self.cantidad_prestada))
            
            # Actualizar inventario
            query = """
            UPDATE inventario 
            SET cantidad_disponible = cantidad_disponible - %s,
                cantidad_prestada = cantidad_prestada + %s
            WHERE id = %s
            """
            cursor.execute(query, (self.cantidad_prestada, 
                                   self.cantidad_prestada, self.inventario_id))
            
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            print(f"Error en préstamo: {e}")
            return None
        finally:
            cursor.close()
    
    def devolver(self):
        """Devuelve un préstamo y actualiza inventario"""
        connection = self.db.connect()
        cursor = connection.cursor()
        
        try:
            # Actualizar préstamo
            query = """
            UPDATE prestamos_activos 
            SET estado = 'devuelto', fecha_devolucion = NOW() 
            WHERE id = %s
            """
            cursor.execute(query, (self.id,))
            
            # Actualizar inventario
            query = """
            UPDATE inventario 
            SET cantidad_disponible = cantidad_disponible + %s,
                cantidad_prestada = cantidad_prestada - %s
            WHERE id = %s
            """
            cursor.execute(query, (self.cantidad_prestada, 
                                   self.cantidad_prestada, self.inventario_id))
            
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"Error en devolución: {e}")
            return False
        finally:
            cursor.close()
    
    @classmethod
    def get_activos(cls):
        """Obtiene todos los préstamos activos"""
        db = Database()
        query = """
        SELECT p.*, u.username as usuario_nombre, 
               i.item_nombre, l.nombre as laboratorio_nombre
        FROM prestamos_activos p
        JOIN usuarios u ON p.usuario_id = u.id
        JOIN inventario i ON p.inventario_id = i.id
        JOIN laboratorios l ON i.laboratorio_id = l.id
        WHERE p.estado = 'prestado'
        ORDER BY p.fecha_prestamo DESC
        """
        results = db.execute_query(query)
        return [cls._create_with_details(data) for data in results] if results else []
    
    @classmethod
    def _create_with_details(cls, data):
        prestamo = cls(
            id=data['id'],
            solicitud_id=data['solicitud_id'],
            usuario_id=data['usuario_id'],
            inventario_id=data['inventario_id'],
            cantidad_prestada=data['cantidad_prestada'],
            fecha_prestamo=data['fecha_prestamo'],
            fecha_devolucion=data.get('fecha_devolucion'),
            estado=data['estado']
        )
        prestamo.usuario_nombre = data.get('usuario_nombre')
        prestamo.item_nombre = data.get('item_nombre')
        prestamo.laboratorio_nombre = data.get('laboratorio_nombre')
        return prestamo
    
    def to_dict(self):
        return {
            'id': self.id,
            'solicitud_id': self.solicitud_id,
            'usuario_nombre': self.usuario_nombre,
            'item_nombre': self.item_nombre,
            'laboratorio_nombre': self.laboratorio_nombre,
            'cantidad_prestada': self.cantidad_prestada,
            'estado': self.estado,
            'fecha_prestamo': self.fecha_prestamo.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_prestamo else None,
            'fecha_devolucion': self.fecha_devolucion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_devolucion else None
        }