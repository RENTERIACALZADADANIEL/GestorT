from typing import List, Dict

class Usuario:
    def __init__(self, username, password, rol):
        self.username = username
        self.password = password
        self.rol = rol  # "admin" o "maestro"

class Objeto:
    def __init__(self, nombre: str, cantidad_total: int):
        self.nombre = nombre
        self.cantidad_total = cantidad_total
        self.cantidad_disponible = cantidad_total

class Laboratorio:
    def __init__(self, id_lab: int, nombre: str):
        self.id = id_lab
        self.nombre = nombre
        self.objetos: List[Objeto] = []

class Reserva:
    def __init__(self, id_reserva: int, laboratorio_id: int, maestro: str, fecha: str, horario: str):
        self.id = id_reserva
        self.laboratorio_id = laboratorio_id
        self.maestro = maestro
        self.fecha = fecha
        self.horario = horario
        self.asignaciones: Dict[str, str] = {} # Almacena { "Nombre del Alumno": "Nombre del Objeto" }