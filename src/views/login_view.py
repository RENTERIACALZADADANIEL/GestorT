import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers import AuthController

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Laboratorios")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        self.auth_controller = AuthController()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de login"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Iniciar Sesión",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Sistema de Gestión de Laboratorios",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para campos
        fields_frame = tk.Frame(main_frame, bg='#f0f0f0')
        fields_frame.pack(fill='x', pady=10)
        
        # Username
        tk.Label(
            fields_frame,
            text="Usuario:",
            font=('Arial', 11),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            fields_frame,
            font=('Arial', 11),
            bd=2,
            relief='groove'
        )
        self.username_entry.pack(fill='x', pady=(0, 15), ipady=5)
        
        # Password
        tk.Label(
            fields_frame,
            text="Contraseña:",
            font=('Arial', 11),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        pass_frame = tk.Frame(fields_frame, bg='#f0f0f0')
        pass_frame.pack(fill='x', pady=(0, 15))
        self.password_entry = tk.Entry(
            pass_frame,
            font=('Arial', 11),
            show="•",
            bd=2,
            relief='groove'
        )
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=5)
        self._show_pass_login = False
        tk.Button(pass_frame, text="👁", command=self._toggle_pass_login,
                  bg='#f0f0f0', bd=1, cursor='hand2', font=('Arial', 11)
                  ).pack(side='left', padx=(5, 0))
        
        # Frame para botones
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', pady=20)
        
        # Botón Login
        login_button = tk.Button(
            buttons_frame,
            text="Iniciar Sesión",
            command=self.login,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        login_button.pack(fill='x', pady=(0, 10))
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=15)
        
        # Frame de información
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(fill='x')
        
        # Información de prueba
        tk.Label(
            info_frame,
            text="Usuarios de prueba:",
            font=('Arial', 9, 'bold'),
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack()
        
        tk.Label(
            info_frame,
            text="Admin: admin / admin123",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#95a5a6'
        ).pack()
        
        tk.Label(
            info_frame,
            text="Maestro: maestro1 / maestro123",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#95a5a6'
        ).pack()
        
    def _toggle_pass_login(self):
        self._show_pass_login = not self._show_pass_login
        self.password_entry.config(show='' if self._show_pass_login else '•')

        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.login())
    
    def login(self):
        """Maneja el inicio de sesión"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        success, message, user_data = self.auth_controller.login(username, password)
        
        if success:
            messagebox.showinfo("Éxito", message)
            self.root.withdraw()  # Oculta ventana de login
            
            if user_data['rol'] == 'admin':
                self.abrir_admin_view(user_data)
            elif user_data['rol'] == 'maestro':
                self.abrir_maestro_view(user_data)
        else:
            messagebox.showerror("Error", message)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def abrir_admin_view(self, user_data):
        """Abre la vista de administrador"""
        from src.views.admin_view import AdminView  # Importación local para evitar referencia circular
        
        admin_window = tk.Toplevel(self.root)
        admin_app = AdminView(admin_window, user_data, self.volver_login)  # Variable local, no de instancia
    
    def abrir_maestro_view(self, user_data):
        """Abre la vista de maestro"""
        from src.views.maestro_view import MaestroView  # Importación local para evitar referencia circular
        
        maestro_window = tk.Toplevel(self.root)
        maestro_app = MaestroView(maestro_window, user_data, self.volver_login)  # Variable local, no de instancia
    
    def volver_login(self):
        """Vuelve a mostrar la ventana de login"""
        self.root.deiconify()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()