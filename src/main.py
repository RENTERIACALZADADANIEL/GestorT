import flet as ft
from views.view import AppView
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_flet(page: ft.Page):
    AppView(page)

def main():
    ft.app(target=start_flet)

if __name__ == "__main__":
    main()