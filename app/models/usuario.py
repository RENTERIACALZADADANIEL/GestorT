import bcrypt
from app.database import Database

class Usuario:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, hash_: str) -> bool:
        return bcrypt.checkpw(password.encode(), hash_.encode())

    @staticmethod
    def find_by_email(email):
        db = Database()
        return db.fetch_one("SELECT * FROM usuarios WHERE email = %s", (email,))