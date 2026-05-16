from src.models import Laboratorio, Reserva
from datetime import datetime, date, timedelta

class MaestroController:
    def __init__(self):
        self.maestro_actual = None
    
    def set_maestro(self, maestro_data):
        """Establece el maestro actual"""
        self.maestro_actual = maestro_data
    
    # ===== VISUALIZACIÓN DE LABORATORIOS =====
    def obtener_laboratorios_disponibles(self):
        """
        Obtiene solo los laboratorios disponibles para reserva
        Retorna: (success, data)
        """
        try:
            laboratorios = Laboratorio.get_disponibles()
            labs_data = []
            for lab in laboratorios:
                labs_data.append({
                    'id': lab.id,
                    'nombre': lab.nombre,
                    'estado': lab.estado
                })
            return True, labs_data
        except Exception as e:
            return False, f"Error al obtener laboratorios: {str(e)}"
    
    def obtener_todos_laboratorios(self):
        """
        Obtiene todos los laboratorios con su estado
        Retorna: (success, data)
        """
        try:
            laboratorios = Laboratorio.get_all()
            labs_data = []
            for lab in laboratorios:
                labs_data.append({
                    'id': lab.id,
                    'nombre': lab.nombre,
                    'estado': lab.estado
                })
            return True, labs_data
        except Exception as e:
            return False, f"Error al obtener laboratorios: {str(e)}"
    
    # ===== GESTIÓN DE BLOQUES HORARIOS =====
    def obtener_bloques_disponibles(self, laboratorio_id, fecha):
        """
        Obtiene los bloques horarios disponibles para un laboratorio en una fecha
        Retorna: (success, data)
        """
        try:
            # Validar campos
            if not laboratorio_id or not fecha:
                return False, "Laboratorio y fecha son obligatorios"
            
            # Validar que la fecha no sea pasada
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hoy = date.today()
            
            if fecha_obj < hoy:
                return False, "No se pueden hacer reservas en fechas pasadas"
            
            # Verificar que el laboratorio existe y está disponible
            laboratorio = Laboratorio.get_by_id(laboratorio_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            if laboratorio.estado == 'mantenimiento':
                return False, "El laboratorio no está disponible (en mantenimiento)"
            
            # Obtener bloques disponibles
            bloques = Reserva.get_bloques_disponibles(laboratorio_id, fecha)
            
            # Formatear respuesta
            bloques_formateados = []
            for bloque in bloques:
                bloques_formateados.append({
                    'id': bloque['id'],
                    'hora_inicio': str(bloque['hora_inicio']),
                    'hora_fin': str(bloque['hora_fin']),
                    'horario_mostrar': f"{bloque['hora_inicio']} - {bloque['hora_fin']}",
                    'estado': bloque['estado']  # 'disponible' o 'ocupado'
                })
            
            return True, bloques_formateados
            
        except ValueError:
            return False, "Formato de fecha no válido. Use YYYY-MM-DD"
        except Exception as e:
            return False, f"Error al obtener bloques: {str(e)}"
    
    # ===== GESTIÓN DE RESERVAS =====
    def crear_reserva(self, laboratorio_id, fecha, hora_inicio, hora_fin):
        """
        Crea una nueva reserva
        Retorna: (success, message)
        """
        try:
            # Validar campos obligatorios
            if not all([laboratorio_id, fecha, hora_inicio, hora_fin]):
                return False, "Todos los campos son obligatorios"
            
            if not self.maestro_actual:
                return False, "Debe iniciar sesión para reservar"
            
            # Validar formato de fecha
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            except ValueError:
                return False, "Formato de fecha no válido. Use YYYY-MM-DD"
            
            # Validar que no sea fecha pasada
            hoy = date.today()
            if fecha_obj < hoy:
                return False, "No se pueden hacer reservas en fechas pasadas"
            
            # Validar formato de horas
            try:
                hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M:%S').time()
                hora_fin_obj = datetime.strptime(hora_fin, '%H:%M:%S').time()
            except ValueError:
                return False, "Formato de hora no válido. Use HH:MM:SS"
            
            # Validar que hora_fin sea posterior a hora_inicio
            if hora_fin_obj <= hora_inicio_obj:
                return False, "La hora de fin debe ser posterior a la hora de inicio"
            
            # Validar que la diferencia sea de 45 minutos
            inicio_dt = datetime.combine(date.today(), hora_inicio_obj)
            fin_dt = datetime.combine(date.today(), hora_fin_obj)
            diferencia = fin_dt - inicio_dt
            
            if diferencia != timedelta(minutes=45):
                return False, "Cada reserva debe ser exactamente de 45 minutos"
            
            # Verificar que el laboratorio existe y está disponible
            laboratorio = Laboratorio.get_by_id(laboratorio_id)
            if not laboratorio:
                return False, "Laboratorio no encontrado"
            
            if laboratorio.estado == 'mantenimiento':
                return False, "El laboratorio no está disponible (en mantenimiento)"
            
            # Verificar que no haya traslape con el receso (10:00 - 10:20)
            receso_inicio = datetime.strptime('10:00:00', '%H:%M:%S').time()
            receso_fin = datetime.strptime('10:20:00', '%H:%M:%S').time()
            
            if (hora_inicio_obj < receso_fin and hora_fin_obj > receso_inicio):
                return False, "No se puede reservar durante el horario de receso (10:00 - 10:20)"
            
            # Verificar que el horario esté dentro del rango permitido (7:00 - 13:20)
            horario_inicio_permitido = datetime.strptime('07:00:00', '%H:%M:%S').time()
            horario_fin_permitido = datetime.strptime('13:20:00', '%H:%M:%S').time()
            
            if hora_inicio_obj < horario_inicio_permitido or hora_fin_obj > horario_fin_permitido:
                return False, "El horario debe estar entre 7:00 AM y 1:20 PM"
            
            # Crear reserva temporal para verificar disponibilidad
            reserva_temp = Reserva(
                laboratorio_id=laboratorio_id,
                usuario_id=self.maestro_actual['id'],
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            
            # Intentar guardar (el método save ya verifica disponibilidad)
            success, result = reserva_temp.save()
            
            if success:
                laboratorio_nombre = laboratorio.nombre if laboratorio else f"ID:{laboratorio_id}"
                return True, f"Reserva creada exitosamente en {laboratorio_nombre} para el {fecha} de {hora_inicio} a {hora_fin}"
            else:
                return False, result  # result contiene el mensaje de error
                
        except Exception as e:
            return False, f"Error al crear reserva: {str(e)}"
    
    def obtener_mis_reservas(self):
        """
        Obtiene las reservas del maestro actual
        Retorna: (success, data)
        """
        try:
            if not self.maestro_actual:
                return False, "Debe iniciar sesión"
            
            reservas = Reserva.get_by_usuario(self.maestro_actual['id'])
            reservas_data = []
            
            for reserva in reservas:
                hora_inicio = str(reserva.hora_inicio) if reserva.hora_inicio else None
                hora_fin = str(reserva.hora_fin) if reserva.hora_fin else None
                
                reservas_data.append({
                    'id': reserva.id,
                    'laboratorio': reserva.laboratorio_nombre,
                    'fecha': str(reserva.fecha),
                    'hora_inicio': hora_inicio,
                    'hora_fin': hora_fin,
                    'horario_mostrar': f"{hora_inicio} - {hora_fin}" if hora_inicio and hora_fin else "",
                    'estado': reserva.estado
                })
            
            return True, reservas_data
            
        except Exception as e:
            return False, f"Error al obtener reservas: {str(e)}"
    
    def cancelar_mi_reserva(self, reserva_id):
        """
        Cancela una reserva del maestro (solo si es suya)
        Retorna: (success, message)
        """
        try:
            if not self.maestro_actual:
                return False, "Debe iniciar sesión"
            
            reserva = Reserva.get_by_id(reserva_id)
            if not reserva:
                return False, "Reserva no encontrada"
            
            # Verificar que la reserva pertenece al maestro
            if reserva.usuario_id != self.maestro_actual['id']:
                return False, "No puedes cancelar reservas de otros usuarios"
            
            if reserva.estado == 'cancelada':
                return False, "La reserva ya está cancelada"
            
            result = reserva.cancelar()
            if result:
                return True, "Reserva cancelada exitosamente"
            else:
                return False, "Error al cancelar reserva"
                
        except Exception as e:
            return False, f"Error al cancelar: {str(e)}"
    
    def obtener_reserva_por_id(self, reserva_id):
        """
        Obtiene los detalles de una reserva específica
        Retorna: (success, data)
        """
        try:
            reserva = Reserva.get_by_id(reserva_id)
            if not reserva:
                return False, "Reserva no encontrada"
            
            return True, reserva.to_dict()
            
        except Exception as e:
            return False, f"Error al obtener reserva: {str(e)}"