from models.modelo import Laboratorio, Reserva, Usuario, Objeto

class Controller:
    def __init__(self):
        self.laboratorios = []
        self.reservas = []
        self.usuarios = [Usuario("tester", "developer", "admin")] # Usuario maestro por defecto
        self.usuario_actual = None
        self._next_lab_id = 1
        self._next_reserva_id = 1
        
        # Horarios definidos de 7:00 a 1:30
        self.horarios_fijos = [
            "07:00 - 08:30", 
            "08:30 - 10:00", 
            "10:00 - 11:30", 
            "11:30 - 13:30"
        ]

    # --- Gestión de Usuarios ---
    def login(self, u, p):
        for user in self.usuarios:
            if user.username == u and user.password == p:
                self.usuario_actual = user
                return True
        return False

    def crear_usuario(self, username, password, rol):
        if any(u.username == username for u in self.usuarios):
            raise ValueError("El nombre de usuario ya existe.")
        self.usuarios.append(Usuario(username, password, rol))
        return True

    # --- Gestión de Laboratorios e Inventario ---
    def agregar_laboratorio(self, nombre):
        nuevo = Laboratorio(self._next_lab_id, nombre)
        self.laboratorios.append(nuevo)
        self._next_lab_id += 1
        return nuevo

    def agregar_objeto(self, lab_id, nombre, cant):
        lab = next((l for l in self.laboratorios if l.id == lab_id), None)
        if lab:
            lab.objetos.append(Objeto(nombre, cant))
            return True
        return False

    # --- Lógica de Reservas ---
    def consultar_disponibilidad(self, lab_id, fecha):
        ocupados = [r.horario for r in self.reservas 
                   if r.laboratorio_id == lab_id and r.fecha == fecha]
        return [h for h in self.horarios_fijos if h not in ocupados]

    def reservar_directo(self, lab_id, maestro, fecha, horario):
        reserva = Reserva(self._next_reserva_id, lab_id, maestro, fecha, horario)
        self.reservas.append(reserva)
        self._next_reserva_id += 1
        return True

    def asignar_objeto_alumno(self, res_id, alumno, nombre_obj):
        res = next((r for r in self.reservas if r.id == res_id), None)
        if not res: raise ValueError("ID de reserva no válido.")
        
        lab = next((l for l in self.laboratorios if l.id == res.laboratorio_id), None)
        obj = next((o for o in lab.objetos if o.nombre == nombre_obj), None)
        
        if obj and obj.cantidad_disponible > 0:
            obj.cantidad_disponible -= 1
            res.asignaciones[alumno] = nombre_obj
            return True
        raise ValueError("Material no disponible o agotado.")