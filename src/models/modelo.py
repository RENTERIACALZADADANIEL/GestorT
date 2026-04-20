from datetime import datetime
from typing import List

class Usuario:
    """Define los usuarios que pueden acceder al sistema."""
    def __init__(self, username, password, rol):
        self.username = username
        self.password = password
        self.rol = rol  # Puede ser "admin" o "maestro"

class Material:
    def __init__(self, nombre: str, cantidad: int):
        self.nombre = nombre
        self.cantidad = cantidad

class Laboratorio:
    def __init__(self, id_lab: int, nombre: str):
        self.id = id_lab
        self.nombre = nombre
        self.materiales: List[Material] = []

class Reserva:
    def __init__(self, laboratorio_id: int, maestro: str, inicio: datetime, fin: datetime):
        self.laboratorio_id = laboratorio_id
        self.maestro = maestro
        self.inicio = inicio
        self.fin = fin