from pydantic import BaseModel, validator, ValidationError
from app.models.turno import Turno

class TurnoCreateSchema(BaseModel):
    laboratorio_id: int
    dia_semana: int  # 1=lunes..7=domingo
    hora_inicio: str  # formato HH:MM
    hora_fin: str

    @validator('dia_semana')
    def dia_valido(cls, v):
        if not 1 <= v <= 7:
            raise ValueError('Día debe ser 1 (lunes) a 7 (domingo)')
        return v

    @validator('hora_fin')
    def hora_fin_mayor(cls, v, values):
        if 'hora_inicio' in values and v <= values['hora_inicio']:
            raise ValueError('hora_fin debe ser mayor que hora_inicio')
        return v

class TurnoController:
    @staticmethod
    def crear_turno(data: dict):
        try:
            validated = TurnoCreateSchema(**data)
            turno_id = Turno.create(
                validated.laboratorio_id,
                validated.dia_semana,
                validated.hora_inicio,
                validated.hora_fin
            )
            return {"success": True, "id": turno_id}
        except ValidationError as e:
            return {"success": False, "errors": e.errors()}
        except Exception as e:
            return {"success": False, "errors": str(e)}

    @staticmethod
    def listar_por_laboratorio(laboratorio_id):
        return Turno.get_by_laboratorio(laboratorio_id)