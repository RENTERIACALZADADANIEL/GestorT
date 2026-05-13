from models.database import Database
import hashlib

class Usuario:
    def __init__(self, id=None, username=None, password=None, rol=None, created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.rol = rol
        self.created_at = created_at
        self.db = Database()
    
    @staticmethod
    def hash_password(password):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def save(self):
        """Crea un nuevo usuario"""
        query = """
        INSERT INTO usuarios (username, password, rol) 
        VALUES (%s, %s, %s)
        """
        params = (
            self.username,
            self.hash_password(self.password),  # Guardar con hash
            self.rol
        )
        return self.db.execute_insert(query, params)
    
    @classmethod
    def get_by_id(cls, user_id):
        """Obtiene un usuario por su ID"""
        db = Database()
        query = "SELECT * FROM usuarios WHERE id = %s"
        result = db.execute_query(query, (user_id,))
        if result:
            user_data = result[0]
            return cls(**user_data)
        return None
    
    @classmethod
    def get_by_username(cls, username):
        """Obtiene un usuario por su nombre de usuario"""
        db = Database()
        query = "SELECT * FROM usuarios WHERE username = %s"
        result = db.execute_query(query, (username,))
        if result:
            user_data = result[0]
            return cls(**user_data)
        return None
    
    @classmethod
    def verify_login(cls, username, password):
        """
        Verifica las credenciales de inicio de sesión
        Primero intenta comparar sin hash (para usuarios existentes)
        Luego intenta con hash (para nuevos usuarios)
        """
        user = cls.get_by_username(username)
        if user:
            # Intentar primero sin hash (texto plano - usuarios antiguos)
            if user.password == password:
                return user
            
            # Intentar con hash (nuevos usuarios registrados con hash)
            if user.password == cls.hash_password(password):
                return user
        
        return None
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los usuarios"""
        db = Database()
        query = "SELECT * FROM usuarios ORDER BY created_at DESC"
        results = db.execute_query(query)
        return [cls(**user_data) for user_data in results] if results else []
    
    def update(self):
        """Actualiza los datos del usuario"""
        query = """
        UPDATE usuarios 
        SET username = %s, rol = %s 
        WHERE id = %s
        """
        params = (self.username, self.rol, self.id)
        return self.db.execute_insert(query, params)
    
    def update_password(self, new_password):
        """Actualiza solo la contraseña (siempre guarda con hash)"""
        query = "UPDATE usuarios SET password = %s WHERE id = %s"
        params = (self.hash_password(new_password), self.id)
        return self.db.execute_insert(query, params)
    
    def delete(self):
        """Elimina el usuario"""
        query = "DELETE FROM usuarios WHERE id = %s"
        return self.db.execute_insert(query, (self.id,))
    
    def to_dict(self):
        """Convierte el objeto a diccionario (sin password)"""
        return {
            'id': self.id,
            'username': self.username,
            'rol': self.rol,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }