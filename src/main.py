import tkinter as tk
import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.views.login_view import LoginView  # 👈 Importa tu archivo login_view.py

def main():
    """
    Función principal que inicia la aplicación
    """
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Iniciar con la vista de login
        app = LoginView(root)  # 👈 Usa la clase LoginView de login_view.py
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()