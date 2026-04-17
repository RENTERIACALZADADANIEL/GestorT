from datetime import datetime
from typing import List

class Material:
    # ... (mismo código que antes)
    """Representa un material dentro de un laboratorio."""
    def __init__(self, nombre: str, cantidad: int):
        self.nombre = nombre
        self.cantidad = cantidad

class Laboratorio:
    """Representa un laboratorio con su lista de materiales."""
    def __init__(self, id_lab: int, nombre: str):
        self.id = id_lab
        self.nombre = nombre
        self.materiales: List[Material] = []  # Inicialmente vacío

class Reserva:
    """Representa la reserva de un laboratorio por un maestro en un horario."""
    def __init__(self, laboratorio_id: int, maestro: str, inicio: datetime, fin: datetime):
        self.laboratorio_id = laboratorio_id
        self.maestro = maestro
        self.inicio = inicio
        self.fin = fin