from datetime import datetime
from typing import List, Optional
from models.modelo import Laboratorio, Reserva, Usuario

class Controller:
    def __init__(self):
        # Datos en memoria (Se reinician al cerrar la app)
        self.laboratorios: List[Laboratorio] = []
        self.reservas: List[Reserva] = []
        self.usuarios: List[Usuario] = [
            Usuario("tester", "developer", "admin")  # Usuario inicial obligatorio
        ]
        self._next_lab_id = 1
        self.usuario_actual: Optional[Usuario] = None

    # --- Lógica de Autenticación ---
    def login(self, username, password) -> bool:
        for u in self.usuarios:
            if u.username == username and u.password == password:
                self.usuario_actual = u
                return True
        return False

    def crear_usuario(self, username, password, rol) -> bool:
        """Solo permite crear usuarios si el usuario actual es admin."""
        if not self.usuario_actual or self.usuario_actual.rol != "admin":
            raise PermissionError("No tienes permisos para crear usuarios.")
        
        if any(u.username == username for u in self.usuarios):
            raise ValueError("El nombre de usuario ya existe.")
            
        nuevo = Usuario(username, password, rol)
        self.usuarios.append(nuevo)
        return True

    # --- Lógica de Negocio ---
    def agregar_laboratorio(self, nombre: str) -> Laboratorio:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        nuevo = Laboratorio(self._next_lab_id, nombre.strip())
        self.laboratorios.append(nuevo)
        self._next_lab_id += 1
        return nuevo

    def obtener_laboratorios(self) -> List[Laboratorio]:
        return self.laboratorios.copy()

    def reservar(self, laboratorio_id: int, maestro: str, inicio: datetime, fin: datetime) -> Optional[Reserva]:
        # Verificar superposición de horarios
        for r in self.reservas:
            if r.laboratorio_id == laboratorio_id:
                if not (fin <= r.inicio or inicio >= r.fin):
                    return None
        
        nueva_reserva = Reserva(laboratorio_id, maestro, inicio, fin)
        self.reservas.append(nueva_reserva)
        return nueva_reserva