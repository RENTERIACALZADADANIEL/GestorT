import flet as ft
from datetime import datetime, timedelta
from controller.controllers import Controller

class AppView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = Controller()
        self.page.title = "Gestor de Laboratorio"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.bgcolor = ft.Colors.GREY_100
        self.mostrar_pantalla_inicial()

    def mostrar_pantalla_inicial(self):
        """Pantalla con botones para elegir rol."""
        self.page.clean()
        titulo = ft.Text("Gestor de Laboratorio", size=32, weight=ft.FontWeight.BOLD)
        
        btn_encargado = ft.ElevatedButton(
            "Encargado", 
            on_click=lambda _: self.mostrar_panel_encargado(), 
            icon=ft.Icons.SETTINGS
        )
        btn_maestro = ft.ElevatedButton(
            "Maestro", 
            on_click=lambda _: self.mostrar_panel_maestro(), 
            icon=ft.Icons.SCHOOL
        )
        
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [titulo, btn_encargado, btn_maestro], 
                    alignment=ft.MainAxisAlignment.CENTER, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    spacing=20
                ),
                padding=50,
            )
        )

    def mostrar_panel_encargado(self):
        """Panel para el encargado: agregar laboratorio y listar existentes."""
        self.page.clean()
        titulo = ft.Text("Panel del Encargado", size=28, weight=ft.FontWeight.BOLD)
        
        txt_nombre = ft.TextField(label="Nombre del laboratorio", width=300)
        lista_labs = ft.ListView(expand=True, spacing=10)
        
        btn_agregar = ft.ElevatedButton(
            "Agregar laboratorio", 
            on_click=lambda _: self.agregar_laboratorio(txt_nombre, lista_labs)
        )
        
        btn_volver = ft.TextButton("← Volver", on_click=lambda _: self.mostrar_pantalla_inicial())
        
        # PASO 1: Agregar a la página
        self.page.add(
            ft.Column([
                titulo,
                ft.Row([txt_nombre, btn_agregar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Laboratorios registrados:", size=20, weight=ft.FontWeight.W_500),
                ft.Container(
                    lista_labs, 
                    height=300, 
                    border=ft.border.all(1, ft.Colors.GREY_400), 
                    border_radius=10, 
                    padding=10
                ),
                btn_volver
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        # PASO 2: Ahora que existe en la página, actualizamos
        self.actualizar_lista_laboratorios(lista_labs)

    def mostrar_panel_maestro(self):
        """Panel para el maestro: listar laboratorios y reservar uno."""
        self.page.clean()
        titulo = ft.Text("Panel del Maestro", size=28, weight=ft.FontWeight.BOLD)
        
        lista_labs = ft.ListView(expand=True, spacing=10, height=200)
        txt_id_lab = ft.TextField(label="ID del laboratorio", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        txt_maestro = ft.TextField(label="Nombre del maestro", width=200)
        btn_reservar = ft.ElevatedButton("Reservar", on_click=lambda _: self.realizar_reserva(txt_id_lab, txt_maestro))
        btn_volver = ft.TextButton("← Volver", on_click=lambda _: self.mostrar_pantalla_inicial())
        
        # PASO 1: Agregar a la página
        self.page.add(
            ft.Column([
                titulo,
                ft.Text("Laboratorios disponibles:", size=18, weight=ft.FontWeight.W_500),
                ft.Container(
                    lista_labs, 
                    border=ft.border.all(1, ft.Colors.GREY_400), 
                    border_radius=10, 
                    padding=10
                ),
                ft.Divider(height=20),
                ft.Text("Reservar laboratorio", size=20, weight=ft.FontWeight.W_500),
                ft.Row([txt_id_lab, txt_maestro, btn_reservar], alignment=ft.MainAxisAlignment.CENTER),
                btn_volver
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        # PASO 2: Actualizar
        self.actualizar_lista_laboratorios(lista_labs)

    def agregar_laboratorio(self, txt_nombre: ft.TextField, lista_labs: ft.ListView):
        nombre = txt_nombre.value
        if not nombre:
            self.mostrar_snackbar("Error: El nombre no puede estar vacío", ft.Colors.RED)
            return
        try:
            self.controller.agregar_laboratorio(nombre)
            self.mostrar_snackbar(f"Laboratorio '{nombre}' agregado", ft.Colors.GREEN)
            txt_nombre.value = ""
            txt_nombre.update()
            self.actualizar_lista_laboratorios(lista_labs)
        except ValueError as e:
            self.mostrar_snackbar(str(e), ft.Colors.RED)

    def actualizar_lista_laboratorios(self, lista_labs: ft.ListView):
        lista_labs.controls.clear()
        labs = self.controller.obtener_laboratorios()
        if not labs:
            lista_labs.controls.append(ft.Text("No hay laboratorios registrados.", italic=True))
        else:
            for lab in labs:
                lista_labs.controls.append(
                    ft.Container(
                        content=ft.Text(f"ID: {lab.id} - {lab.nombre}"),
                        bgcolor=ft.Colors.WHITE,
                        padding=10,
                        border_radius=8,
                    )
                )
        if lista_labs.page:
            lista_labs.update()

    def realizar_reserva(self, txt_id: ft.TextField, txt_maestro: ft.TextField):
        try:
            lab_id = int(txt_id.value.strip())
            nombre_maestro = txt_maestro.value.strip()
            
            if not nombre_maestro:
                self.mostrar_snackbar("Error: Nombre requerido", ft.Colors.RED)
                return

            ahora = datetime.now()
            reserva = self.controller.reservar(lab_id, nombre_maestro, ahora, ahora + timedelta(hours=2))
            
            if reserva:
                self.mostrar_snackbar("✅ Reserva exitosa", ft.Colors.GREEN)
                txt_id.value = ""
                txt_maestro.value = ""
                self.page.update()
            else:
                self.mostrar_snackbar("❌ No disponible", ft.Colors.RED)
        except Exception:
            self.mostrar_snackbar("Error en los datos", ft.Colors.RED)

    def mostrar_snackbar(self, mensaje: str, color: str):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(mensaje), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()