from .database import Database

class Laboratorio:
    def __init__(self, id=None, nombre=None, estado='disponible', created_at=None):
        self.id = id
        self.nombre = nombre
        self.estado = estado
        self.created_at = created_at
        self.db = Database()
    
    def save(self):
        """Crea un nuevo laboratorio"""
        query = """
        INSERT INTO laboratorios (nombre, estado) 
        VALUES (%s, %s)
        """
        params = (self.nombre, self.estado)
        return self.db.execute_insert(query, params)
    
    @classmethod
    def get_by_id(cls, lab_id):
        """Obtiene un laboratorio por su ID"""
        db = Database()
        query = "SELECT * FROM laboratorios WHERE id = %s"
        result = db.execute_query(query, (lab_id,))
        if result:
            return cls(**result[0])
        return None
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los laboratorios"""
        db = Database()
        query = "SELECT * FROM laboratorios ORDER BY created_at DESC"
        results = db.execute_query(query)
        return [cls(**lab_data) for lab_data in results] if results else []
    
    @classmethod
    def get_by_estado(cls, estado):
        """Obtiene laboratorios filtrados por estado"""
        db = Database()
        query = "SELECT * FROM laboratorios WHERE estado = %s ORDER BY nombre"
        results = db.execute_query(query, (estado,))
        return [cls(**lab_data) for lab_data in results] if results else []
    
    @classmethod
    def get_disponibles(cls):
        """Obtiene solo laboratorios disponibles"""
        return cls.get_by_estado('disponible')
    
    def update(self):
        """Actualiza los datos del laboratorio"""
        query = """
        UPDATE laboratorios 
        SET nombre = %s, estado = %s 
        WHERE id = %s
        """
        params = (self.nombre, self.estado, self.id)
        return self.db.execute_insert(query, params)
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del laboratorio"""
        if nuevo_estado in ['disponible', 'mantenimiento']:
            self.estado = nuevo_estado
            query = "UPDATE laboratorios SET estado = %s WHERE id = %s"
            return self.db.execute_insert(query, (nuevo_estado, self.id))
        return False
    
    def delete(self):
        """Elimina el laboratorio"""
        query = "DELETE FROM laboratorios WHERE id = %s"
        return self.db.execute_insert(query, (self.id,))
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estado': self.estado,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }