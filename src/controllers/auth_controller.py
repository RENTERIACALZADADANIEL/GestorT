from src.models import Usuario
from datetime import datetime

class AuthController:
    def __init__(self):
        self.usuario_actual = None
    
    def login(self, username, password):
        """
        Inicia sesión de usuario
        Retorna: (success, message, user_data)
        """
        try:
            # Validar campos vacíos
            if not username or not password:
                return False, "Todos los campos son obligatorios", None
            
            # Verificar credenciales
            usuario = Usuario.verify_login(username, password)
            
            if usuario:
                self.usuario_actual = usuario
                user_data = usuario.to_dict()
                return True, f"Bienvenido {usuario.username}", user_data
            else:
                return False, "Usuario o contraseña incorrectos", None
                
        except Exception as e:
            return False, f"Error al iniciar sesión: {str(e)}", None
    
    def registrar_usuario(self, username, password, rol, admin_id=None):
        """
        Registra un nuevo usuario (solo admin puede crear usuarios)
        Retorna: (success, message)
        """
        try:
            # Validar campos vacíos
            if not username or not password or not rol:
                return False, "Todos los campos son obligatorios"
            
            # Validar rol
            if rol not in ['admin', 'maestro']:
                return False, "Rol no válido"
            
            # Verificar si el usuario ya existe
            usuario_existente = Usuario.get_by_username(username)
            if usuario_existente:
                return False, "El nombre de usuario ya existe"
            
            # Validar longitud de contraseña
            if len(password) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            
            # Crear nuevo usuario
            nuevo_usuario = Usuario(
                username=username,
                password=password,
                rol=rol
            )
            
            result = nuevo_usuario.save()
            
            if result:
                return True, f"Usuario {username} creado exitosamente"
            else:
                return False, "Error al crear el usuario"
                
        except Exception as e:
            return False, f"Error al registrar usuario: {str(e)}"
    
    def logout(self):
        """Cierra la sesión actual"""
        self.usuario_actual = None
        return True, "Sesión cerrada exitosamente"
    
    def get_usuarios(self):
        """Obtiene todos los usuarios (para admin)"""
        try:
            usuarios = Usuario.get_all()
            return True, [usuario.to_dict() for usuario in usuarios]
        except Exception as e:
            return False, f"Error al obtener usuarios: {str(e)}"
    
    def eliminar_usuario(self, user_id, admin_id):
        """
        Elimina un usuario (solo admin)
        Retorna: (success, message)
        """
        try:
            # No permitir que un admin se elimine a sí mismo
            if user_id == admin_id:
                return False, "No puedes eliminar tu propio usuario"
            
            usuario = Usuario.get_by_id(user_id)
            if not usuario:
                return False, "Usuario no encontrado"
            
            result = usuario.delete()
            if result:
                return True, f"Usuario {usuario.username} eliminado exitosamente"
            else:
                return False, "Error al eliminar usuario"
                
        except Exception as e:
            return False, f"Error al eliminar usuario: {str(e)}"
    
    def admin_cambiar_password(self, user_id, new_password, admin_id):
        """
        El admin cambia la contraseña de cualquier usuario sin necesitar la actual
        Retorna: (success, message)
        """
        try:
            if not new_password:
                return False, "La contraseña no puede estar vacía"

            if len(new_password) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"

            if user_id == admin_id:
                return False, "Usa 'cambiar contraseña' para modificar tu propia cuenta"

            usuario = Usuario.get_by_id(user_id)
            if not usuario:
                return False, "Usuario no encontrado"

            result = usuario.update_password(new_password)
            if result:
                return True, f"Contraseña de '{usuario.username}' actualizada correctamente"
            else:
                return False, "Error al actualizar la contraseña"

        except Exception as e:
            return False, f"Error: {str(e)}"

    def cambiar_password(self, user_id, old_password, new_password):
        """
        Cambia la contraseña de un usuario
        Retorna: (success, message)
        """
        try:
            # Validar campos
            if not old_password or not new_password:
                return False, "Todos los campos son obligatorios"
            
            if len(new_password) < 6:
                return False, "La nueva contraseña debe tener al menos 6 caracteres"
            
            # Verificar usuario
            usuario = Usuario.get_by_id(user_id)
            if not usuario:
                return False, "Usuario no encontrado"
            
            # Verificar contraseña actual
            if usuario.password != Usuario.hash_password(old_password):
                return False, "Contraseña actual incorrecta"
            
            # Actualizar contraseña
            result = usuario.update_password(new_password)
            if result:
                return True, "Contraseña actualizada exitosamente"
            else:
                return False, "Error al actualizar contraseña"
                
        except Exception as e:
            return False, f"Error al cambiar contraseña: {str(e)}"