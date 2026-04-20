import flet as ft
from views.view import AppView
import sys
import os

# Configuración de ruta para que detecte los módulos en src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_flet(page: ft.Page):
    """Inicia la interfaz gráfica pasándole la página a la Vista."""
    AppView(page)

def main():
    """Entry point llamado por uv run app."""
    ft.app(target=start_flet)

if __name__ == "__main__":
    main()