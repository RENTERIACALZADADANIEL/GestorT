import tkinter as tk
from tkinter import messagebox, ttk
from controllers import AuthController

class RegistroView:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.auth_controller = AuthController()
        
        # Crear ventana modal
        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Nuevo Usuario")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        self.window.configure(bg='#ecf0f1')
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de registro"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Título
        tk.Label(
            main_frame,
            text="Registrar Nuevo Usuario",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        # Username
        tk.Label(main_frame, text="Usuario:", font=('Arial', 10), bg='#ecf0f1').pack(anchor='w', pady=(0, 5))
        self.username_entry = tk.Entry(main_frame, font=('Arial', 10), width=40)
        self.username_entry.pack(pady=(0, 10), ipady=3)
        
        # Password
        tk.Label(main_frame, text="Contraseña:", font=('Arial', 10), bg='#ecf0f1').pack(anchor='w', pady=(0, 5))
        self.password_entry = tk.Entry(main_frame, font=('Arial', 10), show="•", width=40)
        self.password_entry.pack(pady=(0, 10), ipady=3)
        
        # Rol
        tk.Label(main_frame, text="Rol:", font=('Arial', 10), bg='#ecf0f1').pack(anchor='w', pady=(0, 5))
        self.rol_var = tk.StringVar(value='maestro')
        rol_combo = ttk.Combobox(
            main_frame,
            textvariable=self.rol_var,
            values=['admin', 'maestro'],
            state='readonly',
            width=37
        )
        rol_combo.pack(pady=(0, 20))
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        btn_frame.pack(fill='x')
        
        tk.Button(
            btn_frame,
            text="Registrar",
            command=self.registrar,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        ).pack(side='left', expand=True, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.window.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        ).pack(side='left', expand=True, padx=5)
    
    def registrar(self):
        """Registra un nuevo usuario"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        rol = self.rol_var.get()
        
        success, message = self.auth_controller.registrar_usuario(username, password, rol)
        
        if success:
            messagebox.showinfo("Éxito", message)
            self.callback()  # Actualizar lista de usuarios
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)