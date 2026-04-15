import flet as ft
from app.views.login_view import login_view
from app.views.dashboard_view import dashboard_view

def main(page: ft.Page):
    page.title = "Gestor de Laboratorios"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def go_to_dashboard():
        page.views.clear()
        page.views.append(dashboard_view(page))
        page.go("/dashboard")
        page.update()

    def route_change(route):
        # Si no hay usuario logueado y no estamos en login, redirigir
        user = page.session.get("user")
        if not user and page.route != "/":
            page.go("/")
            return

        if page.route == "/":
            page.views.clear()
            page.views.append(login_view(page, go_to_dashboard))
        elif page.route == "/dashboard":
            if not page.views or page.views[-1].route != "/dashboard":
                page.views.append(dashboard_view(page))
        # Aquí añadir más rutas para laboratorios, turnos, etc.
        page.update()

    page.on_route_change = route_change
    page.go("/")

def run():
    ft.app(target=main)

if __name__ == "__main__":
    run()