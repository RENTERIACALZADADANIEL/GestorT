from datetime import datetime
from typing import List, Optional
from models.modelo import Laboratorio, Reserva

class Controller:
    # ... (mismo código que antes)
    def __init__(self):
        # Almacenamiento en memoria
        self.laboratorios: List[Laboratorio] = []
        self.reservas: List[Reserva] = []
        self._next_lab_id = 1

    def agregar_laboratorio(self, nombre: str) -> Laboratorio:
        """Crea un nuevo laboratorio con ID autoincremental."""
        if not nombre.strip():
            raise ValueError("El nombre del laboratorio no puede estar vacío")
        nuevo = Laboratorio(self._next_lab_id, nombre.strip())
        self.laboratorios.append(nuevo)
        self._next_lab_id += 1
        return nuevo

    def obtener_laboratorios(self) -> List[Laboratorio]:
        """Devuelve la lista de todos los laboratorios."""
        return self.laboratorios.copy()

    def verificar_disponibilidad(self, laboratorio_id: int, inicio: datetime, fin: datetime) -> bool:
        """
        Retorna True si el laboratorio está disponible en el rango [inicio, fin).
        Un laboratorio está disponible si no existe ninguna reserva que se superponga.
        """
        for r in self.reservas:
            if r.laboratorio_id == laboratorio_id:
                # Hay superposición si los intervalos se intersectan
                if not (fin <= r.inicio or inicio >= r.fin):
                    return False
        return True

    def reservar(self, laboratorio_id: int, maestro: str, inicio: datetime, fin: datetime) -> Optional[Reserva]:
        """
        Intenta reservar el laboratorio. Si está disponible, crea y guarda la reserva.
        Retorna la reserva creada o None si no está disponible.
        """
        if not self.verificar_disponibilidad(laboratorio_id, inicio, fin):
            return None
        reserva = Reserva(laboratorio_id, maestro, inicio, fin)
        self.reservas.append(reserva)
        return reserva