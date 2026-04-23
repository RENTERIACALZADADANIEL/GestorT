import flet as ft
from datetime import datetime, timedelta

class AppView:
    def __init__(self, page: ft.Page):
        self.page = page
        from controller.controllers import Controller
        self.controller = Controller()
        
        # Configuración de apariencia
        self.page.title = "Gestor de Laboratorios"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.mostrar_login()

    def mensaje(self, texto, color="blue"):
        self.page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_login(self):
        self.page.clean()
        u = ft.TextField(label="Usuario", width=300, prefix_icon=ft.Icons.PERSON)
        p = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, prefix_icon=ft.Icons.LOCK)
        
        def log(_):
            if self.controller.login(u.value, p.value):
                self.mostrar_menu()
            else:
                self.mensaje("Acceso denegado", "red")

        self.page.add(
            ft.Icon(ft.Icons.SCIENCE, size=50, color="blue"),
            ft.Text("INICIO DE SESIÓN", size=25, weight="bold"),
            u, p,
            ft.ElevatedButton("Entrar", on_click=log, width=300, bgcolor="blue", color="white")
        )

    def mostrar_menu(self):
        self.page.clean()
        rol = self.controller.usuario_actual.rol
        btns = []
        
        if rol == "admin":
            btns.append(ft.ElevatedButton("Gestionar Laboratorios", icon=ft.Icons.SETTINGS, on_click=lambda _: self.panel_admin(), width=280))
            btns.append(ft.ElevatedButton("Registrar Usuarios", icon=ft.Icons.PERSON_ADD, on_click=lambda _: self.panel_usuarios(), width=280))
        
        btns.append(ft.ElevatedButton("Reservas e Inventario", icon=ft.Icons.CALENDAR_MONTH, on_click=lambda _: self.panel_maestro(), width=280))
        btns.append(ft.TextButton("Cerrar Sesión", icon=ft.Icons.EXIT_TO_APP, on_click=lambda _: self.mostrar_login()))

        self.page.add(
            ft.Text(f"PANEL DE {rol.upper()}", size=20, weight="bold"),
            ft.Column(btns, horizontal_alignment="center")
        )

    def panel_usuarios(self):
        self.page.clean()
        u_name = ft.TextField(label="Nuevo Usuario", width=300)
        u_pass = ft.TextField(label="Contraseña", password=True, width=300)
        u_rol = ft.Dropdown(label="Rol", width=300, options=[
            ft.dropdown.Option("admin"), ft.dropdown.Option("maestro")
        ])

        def crear(_):
            try:
                if u_name.value and u_pass.value and u_rol.value:
                    self.controller.crear_usuario(u_name.value, u_pass.value, u_rol.value)
                    self.mensaje(f"Usuario {u_name.value} creado", "green")
                    self.mostrar_menu()
            except Exception as e: self.mensaje(str(e), "red")

        self.page.add(
            ft.Text("REGISTRO DE USUARIOS", weight="bold"),
            u_name, u_pass, u_rol,
            ft.ElevatedButton("Guardar Usuario", on_click=crear, width=300),
            ft.TextButton("Volver", on_click=lambda _: self.mostrar_menu())
        )

    def panel_admin(self):
        self.page.clean()
        t_nombre = ft.TextField(label="Nombre del Laboratorio", width=300)
        
        dd_labs = ft.Dropdown(label="Laboratorio Destino", width=300,
                             options=[ft.dropdown.Option(key=str(l.id), text=l.nombre) for l in self.controller.laboratorios])
        t_obj = ft.TextField(label="Nombre del Objeto", width=180)
        t_can = ft.TextField(label="Cantidad", width=100)

        def add_l(_):
            if t_nombre.value:
                self.controller.agregar_laboratorio(t_nombre.value)
                self.panel_admin()
            
        def add_o(_):
            if dd_labs.value and t_obj.value:
                self.controller.agregar_objeto(int(dd_labs.value), t_obj.value, int(t_can.value))
                self.mensaje("Inventario actualizado", "blue")

        self.page.add(
            ft.Text("CONFIGURACIÓN DE LABORATORIOS", weight="bold"),
            ft.Row([t_nombre, ft.IconButton(ft.Icons.ADD, on_click=add_l)], alignment="center"),
            ft.Divider(),
            ft.Text("AÑADIR MATERIAL"),
            dd_labs,
            ft.Row([t_obj, t_can, ft.IconButton(ft.Icons.SAVE, on_click=add_o)], alignment="center"),
            ft.TextButton("Volver al Menú", on_click=lambda _: self.mostrar_menu())
        )

    def panel_maestro(self):
        self.page.clean()
        dd_lab = ft.Dropdown(label="Laboratorio", width=200, 
                            options=[ft.dropdown.Option(key=str(l.id), text=l.nombre) for l in self.controller.laboratorios])
        
        hoy = datetime.now()
        fechas = [(hoy + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        dd_fecha = ft.Dropdown(label="Fecha", width=150, options=[ft.dropdown.Option(f) for f in fechas])
        dd_hora = ft.Dropdown(label="Horario", width=200)

        def actualizar_h(_):
            if dd_lab.value and dd_fecha.value:
                libres = self.controller.consultar_disponibilidad(int(dd_lab.value), dd_fecha.value)
                dd_hora.options = [ft.dropdown.Option(h) for h in libres]
                dd_hora.update()

        dd_lab.on_change = actualizar_h
        dd_fecha.on_change = actualizar_h

        def reservar(_):
            if dd_hora.value:
                self.controller.reservar_directo(int(dd_lab.value), self.controller.usuario_actual.username, dd_fecha.value, dd_hora.value)
                self.mensaje("Reserva confirmada", "green")
                self.mostrar_menu()

        # Asignación
        t_rid = ft.TextField(label="ID Reserva", width=100)
        t_alu = ft.TextField(label="Alumno", width=180)
        t_obj = ft.TextField(label="Material", width=150)
        
        def asignar(_):
            try:
                self.controller.asignar_objeto_alumno(int(t_rid.value), t_alu.value, t_obj.value)
                self.mensaje("Asignación registrada", "green")
            except Exception as e: self.mensaje(str(e), "red")

        self.page.add(
            ft.Text("RESERVAS Y ASIGNACIONES", size=20, weight="bold"),
            ft.Row([dd_lab, dd_fecha], alignment="center"),
            ft.Row([dd_hora, ft.ElevatedButton("Reservar", on_click=reservar)], alignment="center"),
            ft.Divider(),
            ft.Text("ASIGNAR MATERIAL A ALUMNO"),
            ft.Row([t_rid, t_alu, t_obj], alignment="center"),
            ft.ElevatedButton("Registrar Entrega", on_click=asignar, width=200),
            ft.TextButton("Volver", on_click=lambda _: self.mostrar_menu())
        )