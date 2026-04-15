import bcrypt
from app.database import Database

class Usuario:
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash bcrypt de una contraseña."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifica contraseña contra hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def find_by_email(email: str):
        db = Database()
        query = "SELECT id, nombre, email, rol, password_hash FROM usuarios WHERE email = %s"
        return db.fetch_one(query, (email,))

    @staticmethod
    def create(nombre: str, email: str, password: str, rol: str):
        hashed = Usuario.hash_password(password)
        db = Database()
        query = "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (%s, %s, %s, %s)"
        db.execute_query(query, (nombre, email, hashed, rol))
        return db.cursor.lastrowid  # Necesitas modificar database.py para obtener lastrowid