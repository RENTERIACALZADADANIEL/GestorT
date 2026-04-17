import flet as ft
from views.view import AppView

# Esta es la función que Flet usará internamente
def start_flet(page: ft.Page):
    AppView(page)

# Esta es la función que llamará UV (sin argumentos)
def main():
    ft.app(target=start_flet)

if __name__ == "__main__":
    main()