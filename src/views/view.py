import flet as ft
from datetime import datetime, timedelta

class AppView:
    def __init__(self, page: ft.Page):
        self.page = page
        from controller.controllers import Controller
        self.controller = Controller()
        
        self.page.title = "Sistema GestorT"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        self.mostrar_login()

    def mostrar_snackbar(self, mensaje: str, color: str):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(mensaje), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    # --- VISTA: LOGIN ---
    def mostrar_login(self):
        self.page.clean()
        
        txt_user = ft.TextField(label="Usuario", width=300, prefix_icon=ft.Icons.PERSON)
        txt_pass = ft.TextField(label="Contraseña", width=300, password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
        
        def intentar_login(_):
            if self.controller.login(txt_user.value, txt_pass.value):
                self.mostrar_pantalla_inicial()
            else:
                self.mostrar_snackbar("Usuario o contraseña incorrectos", ft.Colors.RED)

        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.LOCK_PERSON, size=50, color=ft.Colors.BLUE),
                    ft.Text("Inicio de Sesión", size=30, weight="bold"),
                    txt_user,
                    txt_pass,
                    ft.ElevatedButton("Entrar", on_click=intentar_login, width=300),
                ], horizontal_alignment="center", spacing=20),
                padding=40,
                border_radius=20,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_200)
            )
        )

    # --- VISTA: MENÚ PRINCIPAL ---
    def mostrar_pantalla_inicial(self):
        self.page.clean()
        user = self.controller.usuario_actual
        
        botones = []
        
        # Opciones exclusivas de Admin
        if user.rol == "admin":
            botones.append(ft.ElevatedButton("Gestionar Laboratorios", icon=ft.Icons.SETTINGS, on_click=lambda _: self.mostrar_panel_encargado()))
            botones.append(ft.ElevatedButton("Gestionar Usuarios", icon=ft.Icons.GROUP_ADD, on_click=lambda _: self.mostrar_panel_usuarios()))
        
        # Opción para todos (Maestros y Admins)
        botones.append(ft.ElevatedButton("Panel de Reservas", icon=ft.Icons.CALENDAR_MONTH, on_click=lambda _: self.mostrar_panel_maestro()))
        botones.append(ft.TextButton("Cerrar Sesión", on_click=lambda _: self.mostrar_login(), icon=ft.Icons.LOGOUT))

        self.page.add(
            ft.Column([
                ft.Text(f"Bienvenido, {user.username}", size=28, weight="bold"),
                ft.Text(f"Rol: {user.rol.upper()}", color=ft.Colors.BLUE_GREY),
                ft.Divider(height=20),
                *botones
            ], horizontal_alignment="center", spacing=15)
        )

    # --- VISTA: GESTIÓN DE USUARIOS (Solo Admin) ---
    def mostrar_panel_usuarios(self):
        self.page.clean()
        
        txt_new_user = ft.TextField(label="Nombre de Usuario", width=300)
        txt_new_pass = ft.TextField(label="Contraseña", width=300)
        dd_rol = ft.Dropdown(
            label="Rol",
            width=300,
            options=[ft.dropdown.Option("admin"), ft.dropdown.Option("maestro")]
        )

        def guardar_usuario(_):
            try:
                if self.controller.crear_usuario(txt_new_user.value, txt_new_pass.value, dd_rol.value):
                    self.mostrar_snackbar("Usuario creado exitosamente", ft.Colors.GREEN)
                    self.mostrar_pantalla_inicial()
            except Exception as e:
                self.mostrar_snackbar(str(e), ft.Colors.RED)

        self.page.add(
            ft.Column([
                ft.Text("Registrar Nuevo Usuario", size=25, weight="bold"),
                txt_new_user, txt_new_pass, dd_rol,
                ft.Row([
                    ft.ElevatedButton("Guardar", on_click=guardar_usuario, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                    ft.TextButton("Cancelar", on_click=lambda _: self.mostrar_pantalla_inicial())
                ], alignment="center")
            ], horizontal_alignment="center", spacing=20)
        )

    # --- VISTA: PANELES EXISTENTES (Encargado y Maestro) ---
    def mostrar_panel_encargado(self):
        self.page.clean()
        txt_nombre = ft.TextField(label="Nombre del laboratorio", width=300)
        lista_labs = ft.ListView(expand=True, spacing=10)
        
        btn_agregar = ft.ElevatedButton("Agregar", on_click=lambda _: self.agregar_laboratorio(txt_nombre, lista_labs))
        btn_volver = ft.TextButton("← Volver", on_click=lambda _: self.mostrar_pantalla_inicial())
        
        self.page.add(
            ft.Column([
                ft.Text("Gestión de Laboratorios", size=28, weight="bold"),
                ft.Row([txt_nombre, btn_agregar], alignment="center"),
                ft.Container(lista_labs, height=300, border=ft.border.all(1), padding=10, border_radius=10),
                btn_volver
            ], horizontal_alignment="center")
        )
        self.actualizar_lista_laboratorios(lista_labs)

    def mostrar_panel_maestro(self):
        self.page.clean()
        lista_labs = ft.ListView(expand=True, spacing=10, height=200)
        txt_id_lab = ft.TextField(label="ID Lab", width=100)
        txt_maestro = ft.TextField(label="Tu Nombre", width=200, value=self.controller.usuario_actual.username)
        
        btn_reservar = ft.ElevatedButton("Reservar (2h)", on_click=lambda _: self.realizar_reserva(txt_id_lab, txt_maestro))
        btn_volver = ft.TextButton("← Volver", on_click=lambda _: self.mostrar_pantalla_inicial())
        
        self.page.add(
            ft.Column([
                ft.Text("Reservar Laboratorio", size=28, weight="bold"),
                ft.Container(lista_labs, border=ft.border.all(1), padding=10, height=200),
                ft.Row([txt_id_lab, txt_maestro, btn_reservar], alignment="center"),
                btn_volver
            ], horizontal_alignment="center")
        )
        self.actualizar_lista_laboratorios(lista_labs)

    def actualizar_lista_laboratorios(self, lista_labs: ft.ListView):
        lista_labs.controls.clear()
        labs = self.controller.obtener_laboratorios()
        if not labs:
            lista_labs.controls.append(ft.Text("No hay laboratorios registrados."))
        else:
            for lab in labs:
                lista_labs.controls.append(ft.Text(f"ID: {lab.id} - {lab.nombre}", size=16))
        if lista_labs.page:
            lista_labs.update()

    def agregar_laboratorio(self, txt, lista):
        try:
            self.controller.agregar_laboratorio(txt.value)
            txt.value = ""
            txt.update()
            self.actualizar_lista_laboratorios(lista)
        except Exception as e:
            self.mostrar_snackbar(str(e), ft.Colors.RED)

    def realizar_reserva(self, tid, tmaestro):
        try:
            inicio = datetime.now()
            fin = inicio + timedelta(hours=2)
            res = self.controller.reservar(int(tid.value), tmaestro.value, inicio, fin)
            if res:
                self.mostrar_snackbar("Reserva realizada", ft.Colors.GREEN)
            else:
                self.mostrar_snackbar("Laboratorio ocupado", ft.Colors.RED)
        except:
            self.mostrar_snackbar("Datos inválidos", ft.Colors.RED)