import flet as ft
from app.controllers.auth_controller import AuthController

def login_view(page: ft.Page, on_login_success):
    email_input = ft.TextField(label="Correo electrónico", width=300)
    pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text("", color=ft.Colors.RED_400)

    def handle_login(e):
        user = AuthController.login(email_input.value.strip(), pass_input.value.strip())
        if user:
            page.session.set("user", user)
            on_login_success()
        else:
            error_text.value = "Credenciales incorrectas"
            page.update()

    return ft.View(
        "/",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.SCIENCE, size=80, color=ft.Colors.BLUE_700),
                        ft.Text("Gestor de Laboratorios", size=32, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        email_input,
                        pass_input,
                        ft.ElevatedButton("Iniciar sesión", on_click=handle_login, width=300),
                        error_text,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )