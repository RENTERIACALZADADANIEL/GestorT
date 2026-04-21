import flet as ft
from datetime import datetime, timedelta

class AppView:
    def __init__(self, page: ft.Page):
        self.page = page
        from controller.controllers import Controller
        self.controller = Controller()
        
        # Configuración de centrado global de la página
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        self.mostrar_login()

    def mostrar_snackbar(self, texto, color):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(texto), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_login(self):
        self.page.clean()
        u = ft.TextField(label="Usuario", width=300)
        p = ft.TextField(label="Contraseña", password=True, width=300)
        def log(_):
            if self.controller.login(u.value, p.value): self.mostrar_menu()
            else: self.mostrar_snackbar("Error", "red")
        
        # Columna centrada para el login
        self.page.add(
            ft.Column([
                ft.Text("LOGIN", size=30, weight="bold"), 
                u, p, 
                ft.ElevatedButton("Entrar", on_click=log, width=300)
            ], horizontal_alignment="center")
        )

    def mostrar_menu(self):
        self.page.clean()
        rol = self.controller.usuario_actual.rol
        btns = []
        if rol == "admin":
            btns.append(ft.ElevatedButton("Labs y Objetos", on_click=lambda _: self.panel_labs_admin(), width=250))
            btns.append(ft.ElevatedButton("Aprobar Reservas", on_click=lambda _: self.panel_aprobar(), width=250))
            btns.append(ft.ElevatedButton("Usuarios", on_click=lambda _: self.panel_usuarios(), width=250))
        
        btns.append(ft.ElevatedButton("Mis Reservas / Asignar", on_click=lambda _: self.panel_maestro(), width=250))
        btns.append(ft.TextButton("Salir", on_click=lambda _: self.mostrar_login()))
        
        # Columna centrada para el menú
        self.page.add(
            ft.Column([
                ft.Text(f"Bienvenido {rol.upper()}", size=25), 
                *btns
            ], horizontal_alignment="center")
        )

    def panel_labs_admin(self):
        self.page.clean()
        t_nombre = ft.TextField(label="Nombre Lab", width=250)
        def add_l(_): 
            self.controller.agregar_laboratorio(t_nombre.value)
            self.panel_labs_admin()
        
        t_lid = ft.TextField(label="ID Lab", width=80)
        t_oname = ft.TextField(label="Objeto", width=150)
        t_ocant = ft.TextField(label="Cant", width=80)
        def add_o(_):
            self.controller.agregar_objeto_a_lab(int(t_lid.value), t_oname.value, int(t_ocant.value))
            self.mostrar_snackbar("Objeto agregado", "blue")

        self.page.add(
            ft.Column([
                ft.Text("Nuevo Lab", size=20),
                ft.Row([t_nombre, ft.Button("Crear", on_click=add_l)], alignment="center"),
                ft.Divider(),
                ft.Text("Añadir Objeto a Lab", size=20),
                ft.Row([t_lid, t_oname, t_ocant, ft.Button("Añadir", on_click=add_o)], alignment="center"),
                ft.TextButton("Volver", on_click=lambda _: self.mostrar_menu())
            ], horizontal_alignment="center")
        )

    def panel_aprobar(self):
        self.page.clean()
        lista = ft.Column(horizontal_alignment="center")
        for r in self.controller.reservas:
            if r.estado == "Pendiente":
                lista.controls.append(
                    ft.Row([
                        ft.Text(f"ID:{r.id} - {r.maestro}"),
                        ft.IconButton(ft.icons.CHECK, color="green", on_click=lambda _, rid=r.id: [self.controller.cambiar_estado_reserva(rid, "Aprobada"), self.panel_aprobar()]),
                        ft.IconButton(ft.icons.CLOSE, color="red", on_click=lambda _, rid=r.id: [self.controller.cambiar_estado_reserva(rid, "Rechazada"), self.panel_aprobar()])
                    ], alignment="center")
                )
        self.page.add(
            ft.Column([
                ft.Text("Aprobar Reservas", size=20),
                lista,
                ft.TextButton("Volver", on_click=lambda _: self.mostrar_menu())
            ], horizontal_alignment="center")
        )

    def panel_maestro(self):
        self.page.clean()
        t_lab = ft.TextField(label="ID Lab para reservar", width=250)
        def res(_):
            self.controller.reservar(int(t_lab.value), self.controller.usuario_actual.username, datetime.now(), datetime.now()+timedelta(hours=2))
            self.mostrar_snackbar("Enviada a aprobación", "orange")

        t_rid = ft.TextField(label="ID Reserva APROBADA", width=250)
        t_alum = ft.TextField(label="Alumno", width=250)
        t_obj = ft.TextField(label="Objeto", width=250)
        def asig(_):
            try:
                self.controller.asignar_objeto_alumno(int(t_rid.value), t_alum.value, t_obj.value)
                self.mostrar_snackbar("Asignado", "green")
            except Exception as e: self.mostrar_snackbar(str(e), "red")

        self.page.add(
            ft.Column([
                ft.Text("Nueva Reserva", size=20),
                ft.Row([t_lab, ft.Button("Reservar", on_click=res)], alignment="center"),
                ft.Divider(),
                ft.Text("Asignar Objeto (Solo Reservas Aprobadas)", size=18),
                t_rid, t_alum, t_obj,
                ft.ElevatedButton("Asignar a Alumno", on_click=asig, width=250),
                ft.TextButton("Volver", on_click=lambda _: self.mostrar_menu())
            ], horizontal_alignment="center")
        )

    def panel_usuarios(self):
        self.page.clean()
        u = ft.TextField(label="Usuario", width=250)
        p = ft.TextField(label="Pass", width=250)
        r = ft.Dropdown(width=250, options=[ft.dropdown.Option("admin"), ft.dropdown.Option("maestro")])
        def save(_):
            self.controller.crear_usuario(u.value, p.value, r.value)
            self.mostrar_menu()
        
        self.page.add(
            ft.Column([
                ft.Text("Gestión de Usuarios", size=20),
                u, p, r,
                ft.Button("Guardar", on_click=save, width=250),
                ft.TextButton("Volver", on_click=lambda _: self.mostrar_menu())
            ], horizontal_alignment="center")
        )