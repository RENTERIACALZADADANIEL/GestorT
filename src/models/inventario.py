from src.models.database import Database

class Inventario:
    def __init__(self, id=None, laboratorio_id=None, item_nombre=None, 
                 cantidad_total=None, cantidad_disponible=None, cantidad_prestada=None,
                 created_at=None, laboratorio_nombre=None):
        self.id = id
        self.laboratorio_id = laboratorio_id
        self.item_nombre = item_nombre
        self.cantidad_total = cantidad_total
        self.cantidad_disponible = cantidad_disponible if cantidad_disponible is not None else cantidad_total
        self.cantidad_prestada = cantidad_prestada if cantidad_prestada is not None else 0
        self.created_at = created_at
        self.laboratorio_nombre = laboratorio_nombre
        self.db = Database()
    
    def save(self):
        """Agrega un nuevo item al inventario"""
        query = """
        INSERT INTO inventario (laboratorio_id, item_nombre, cantidad_total, cantidad_disponible, cantidad_prestada) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self.laboratorio_id, 
            self.item_nombre, 
            self.cantidad_total,
            self.cantidad_total,  # cantidad_disponible = cantidad_total al crear
            0  # cantidad_prestada = 0 al crear
        )
        return self.db.execute_insert(query, params)
    
    @classmethod
    def get_by_id(cls, item_id):
        """Obtiene un item por su ID"""
        db = Database()
        query = """
        SELECT i.*, l.nombre as laboratorio_nombre
        FROM inventario i
        JOIN laboratorios l ON i.laboratorio_id = l.id
        WHERE i.id = %s
        """
        result = db.execute_query(query, (item_id,))
        if result:
            return cls(**result[0])
        return None
    
    @classmethod
    def get_by_laboratorio(cls, laboratorio_id):
        """Obtiene todos los items de un laboratorio"""
        db = Database()
        query = """
        SELECT i.*, l.nombre as laboratorio_nombre
        FROM inventario i
        JOIN laboratorios l ON i.laboratorio_id = l.id
        WHERE i.laboratorio_id = %s
        ORDER BY i.item_nombre
        """
        results = db.execute_query(query, (laboratorio_id,))
        return [cls(**data) for data in results] if results else []
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los items del inventario"""
        db = Database()
        query = """
        SELECT i.*, l.nombre as laboratorio_nombre
        FROM inventario i
        JOIN laboratorios l ON i.laboratorio_id = l.id
        ORDER BY l.nombre, i.item_nombre
        """
        results = db.execute_query(query)
        return [cls(**data) for data in results] if results else []
    
    def update(self):
        """Actualiza un item del inventario"""
        query = """
        UPDATE inventario 
        SET laboratorio_id = %s, item_nombre = %s, cantidad_total = %s,
            cantidad_disponible = %s, cantidad_prestada = %s
        WHERE id = %s
        """
        params = (
            self.laboratorio_id, 
            self.item_nombre, 
            self.cantidad_total,
            self.cantidad_disponible,
            self.cantidad_prestada,
            self.id
        )
        return self.db.execute_insert(query, params)
    
    def actualizar_cantidad(self, nueva_cantidad):
        """Actualiza solo la cantidad total de un item"""
        self.cantidad_total = nueva_cantidad
        self.cantidad_disponible = nueva_cantidad - self.cantidad_prestada
        query = "UPDATE inventario SET cantidad_total = %s, cantidad_disponible = %s WHERE id = %s"
        return self.db.execute_insert(query, (nueva_cantidad, self.cantidad_disponible, self.id))
    
    def delete(self):
        """Elimina un item del inventario"""
        query = "DELETE FROM inventario WHERE id = %s"
        return self.db.execute_insert(query, (self.id,))
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'laboratorio_id': self.laboratorio_id,
            'item_nombre': self.item_nombre,
            'cantidad_total': self.cantidad_total,
            'cantidad_disponible': self.cantidad_disponible if self.cantidad_disponible is not None else self.cantidad_total,
            'cantidad_prestada': self.cantidad_prestada if self.cantidad_prestada is not None else 0,
            'laboratorio_nombre': self.laboratorio_nombre,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }