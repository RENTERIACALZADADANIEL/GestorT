from pydantic import BaseModel, EmailStr, ValidationError
from app.models.usuario import Usuario

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class AuthController:
    @staticmethod
    def login(email: str, password: str):
        # Validar entrada con Pydantic
        try:
            LoginSchema(email=email, password=password)
        except ValidationError:
            return None

        user = Usuario.find_by_email(email)
        if user and Usuario.verify_password(password, user['password_hash']):
            # Retornar dict sin el hash
            return {'id': user['id'], 'nombre': user['nombre'], 'email': user['email'], 'rol': user['rol']}
        return None