from datetime import datetime
from typing import List, Optional
from models.modelo import Laboratorio, Reserva, Usuario, Objeto

class Controller:
    def __init__(self):
        self.laboratorios: List[Laboratorio] = []
        self.reservas: List[Reserva] = []
        self.usuarios: List[Usuario] = [Usuario("tester", "developer", "admin")]
        self.usuario_actual: Optional[Usuario] = None
        self._next_lab_id = 1
        self._next_reserva_id = 1

    # --- Autenticación ---
    def login(self, username, password) -> bool:
        for u in self.usuarios:
            if u.username == username and u.password == password:
                self.usuario_actual = u
                return True
        return False

    def crear_usuario(self, username, password, rol):
        if self.usuario_actual.rol != "admin": return False
        if any(u.username == username for u in self.usuarios): raise ValueError("Ya existe")
        self.usuarios.append(Usuario(username, password, rol))
        return True

    # --- Gestión de Laboratorios y Objetos (Admin) ---
    def agregar_laboratorio(self, nombre: str):
        nuevo = Laboratorio(self._next_lab_id, nombre)
        self.laboratorios.append(nuevo)
        self._next_lab_id += 1
        return nuevo

    def agregar_objeto_a_lab(self, lab_id: int, nombre: str, cantidad: int):
        lab = next((l for l in self.laboratorios if l.id == lab_id), None)
        if lab:
            lab.objetos.append(Objeto(nombre, cantidad))
            return True
        return False

    # --- Gestión de Reservas ---
    def reservar(self, lab_id, maestro, inicio, fin):
        reserva = Reserva(self._next_reserva_id, lab_id, maestro, inicio, fin)
        self.reservas.append(reserva)
        self._next_reserva_id += 1
        return reserva

    def cambiar_estado_reserva(self, res_id, estado):
        res = next((r for r in self.reservas if r.id == res_id), None)
        if res: res.estado = estado

    def asignar_objeto_alumno(self, res_id, alumno, nombre_obj):
        res = next((r for r in self.reservas if r.id == res_id), None)
        if not res or res.estado != "Aprobada":
            raise ValueError("La reserva no está aprobada.")
        
        lab = next((l for l in self.laboratorios if l.id == res.laboratorio_id), None)
        obj = next((o for o in lab.objetos if o.nombre == nombre_obj), None)
        
        if obj and obj.cantidad_disponible > 0:
            obj.cantidad_disponible -= 1
            res.asignaciones[alumno] = nombre_obj
            return True
        raise ValueError("Material no disponible.")

    def obtener_laboratorios(self): return self.laboratorios