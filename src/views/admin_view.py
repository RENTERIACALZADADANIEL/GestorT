import tkinter as tk
from tkinter import messagebox, ttk
from controllers.admin_controller import AdminController 
from controllers.auth_controller import AuthController
from .registro_view import RegistroView

class AdminView:
    def __init__(self, root, user_data, logout_callback):
        self.root = root
        self.root.title(f"Panel de Administrador - {user_data['username']}")
        self.root.geometry("1000x600")
        self.root.configure(bg='#ecf0f1')
        
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.admin_controller = AdminController()
        self.admin_controller.set_admin(user_data)
        self.auth_controller = AuthController()
        
        self.setup_ui()
        self.cargar_dashboard()
    
    def setup_ui(self):
        """Configura la interfaz del administrador"""
        # Barra superior
        top_bar = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_bar.pack(fill='x')
        
        tk.Label(
            top_bar,
            text=f"Bienvenido, {self.user_data['username']} (Admin)",
            font=('Arial', 12, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', padx=20, pady=10)
        
        # Botón Cerrar Sesión
        tk.Button(
            top_bar,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            bd=0,
            padx=20,
            pady=5,
            cursor='hand2'
        ).pack(side='right', padx=20, pady=10)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña Dashboard
        self.tab_dashboard = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_dashboard, text="📊 Dashboard")
        
        # Pestaña Laboratorios
        self.tab_laboratorios = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_laboratorios, text="🔬 Laboratorios")
        
        # Pestaña Usuarios
        self.tab_usuarios = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_usuarios, text="👥 Usuarios")
        
        # Pestaña Inventario
        self.tab_inventario = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_inventario, text="📦 Inventario")
        
        self.setup_dashboard_tab()
        self.setup_laboratorios_tab()
        self.setup_usuarios_tab()
        self.setup_inventario_tab()
    
    def setup_dashboard_tab(self):
        """Configura la pestaña del dashboard"""
        # Frame de control
        control_frame = tk.Frame(self.tab_dashboard, bg='#ecf0f1')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            control_frame,
            text="🔄 Actualizar",
            command=self.cargar_dashboard,
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left')
        
        # Frame para las tarjetas
        self.cards_frame = tk.Frame(self.tab_dashboard, bg='#ecf0f1')
        self.cards_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas y Scrollbar para scroll
        self.canvas_dashboard = tk.Canvas(self.cards_frame, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(self.cards_frame, orient="vertical", command=self.canvas_dashboard.yview)
        self.scrollable_frame = tk.Frame(self.canvas_dashboard, bg='#ecf0f1')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_dashboard.configure(scrollregion=self.canvas_dashboard.bbox("all"))
        )
        
        self.canvas_dashboard.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_dashboard.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_dashboard.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def cargar_dashboard(self):
        """Carga las reservas en el dashboard"""
        # Limpiar frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        success, reservas = self.admin_controller.obtener_dashboard()
        
        if not success:
            tk.Label(
                self.scrollable_frame,
                text="Error al cargar reservas",
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        if not reservas:
            tk.Label(
                self.scrollable_frame,
                text="No hay reservas activas",
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#7f8c8d'
            ).pack(pady=20)
            return
        
        # Crear tarjetas para cada reserva
        row_frame = None
        for i, reserva in enumerate(reservas):
            if i % 3 == 0:
                row_frame = tk.Frame(self.scrollable_frame, bg='#ecf0f1')
                row_frame.pack(fill='x', padx=5, pady=5)
            
            card = tk.Frame(row_frame, bg='white', bd=1, relief='solid', width=280, height=180)
            card.pack(side='left', padx=10, pady=10, fill='both', expand=True)
            card.pack_propagate(False)
            
            # Contenido de la tarjeta
            tk.Label(
                card,
                text=f"📅 {reserva['fecha']}",
                font=('Arial', 11, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(pady=(10, 5))
            
            tk.Label(
                card,
                text=f"⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}",
                font=('Arial', 10),
                bg='white',
                fg='#34495e'
            ).pack(pady=2)
            
            tk.Label(
                card,
                text=f"🔬 {reserva['laboratorio']}",
                font=('Arial', 10),
                bg='white',
                fg='#34495e'
            ).pack(pady=2)
            
            tk.Label(
                card,
                text=f"👤 {reserva['usuario']} ({reserva['rol']})",
                font=('Arial', 10),
                bg='white',
                fg='#34495e'
            ).pack(pady=2)
            
            # Botón cancelar
            tk.Button(
                card,
                text="Cancelar Reserva",
                command=lambda r=reserva: self.cancelar_reserva_dashboard(r['id']),
                font=('Arial', 9),
                bg='#e74c3c',
                fg='white',
                bd=0,
                padx=10,
                pady=3,
                cursor='hand2'
            ).pack(pady=10)
    
    def cancelar_reserva_dashboard(self, reserva_id):
        """Cancela una reserva desde el dashboard"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar esta reserva?"):
            success, message = self.admin_controller.cancelar_reserva(reserva_id)
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_dashboard()
            else:
                messagebox.showerror("Error", message)
    
    def setup_laboratorios_tab(self):
        """Configura la pestaña de laboratorios"""
        # Frame de formulario
        form_frame = tk.LabelFrame(self.tab_laboratorios, text="Crear/Editar Laboratorio", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        form_frame.pack(fill='x', padx=10, pady=10)
        
        form_inner = tk.Frame(form_frame, bg='#ecf0f1')
        form_inner.pack(padx=10, pady=10)
        
        # Nombre
        tk.Label(form_inner, text="Nombre:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        self.lab_nombre_entry = tk.Entry(form_inner, width=40, font=('Arial', 10))
        self.lab_nombre_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Estado
        tk.Label(form_inner, text="Estado:", bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        self.lab_estado_var = tk.StringVar(value='disponible')
        estado_combo = ttk.Combobox(form_inner, textvariable=self.lab_estado_var, values=['disponible', 'mantenimiento'], state='readonly', width=37)
        estado_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Botones
        btn_frame = tk.Frame(form_inner, bg='#ecf0f1')
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        tk.Button(
            btn_frame,
            text="Crear Laboratorio",
            command=self.crear_laboratorio,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        self.edit_lab_btn = tk.Button(
            btn_frame,
            text="Actualizar Seleccionado",
            command=self.actualizar_laboratorio,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            state='disabled'
        )
        self.edit_lab_btn.pack(side='left', padx=5)
        
        # Frame de lista
        list_frame = tk.LabelFrame(self.tab_laboratorios, text="Laboratorios Existentes", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para laboratorios
        columns = ('ID', 'Nombre', 'Estado')
        self.lab_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.lab_tree.heading(col, text=col)
            self.lab_tree.column(col, width=150)
        
        self.lab_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.lab_tree.bind('<<TreeviewSelect>>', self.on_lab_select)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.lab_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.lab_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón eliminar
        tk.Button(
            list_frame,
            text="Eliminar Seleccionado",
            command=self.eliminar_laboratorio,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(pady=10)
        
        self.cargar_laboratorios()
    
    def cargar_laboratorios(self):
        """Carga la lista de laboratorios"""
        for item in self.lab_tree.get_children():
            self.lab_tree.delete(item)
        
        success, laboratorios = self.admin_controller.obtener_laboratorios()
        if success:
            for lab in laboratorios:
                self.lab_tree.insert('', 'end', values=(lab['id'], lab['nombre'], lab['estado']))
    
    def on_lab_select(self, event):
        """Maneja la selección de un laboratorio"""
        selection = self.lab_tree.selection()
        if selection:
            self.edit_lab_btn.config(state='normal')
            item = self.lab_tree.item(selection[0])
            self.lab_nombre_entry.delete(0, tk.END)
            self.lab_nombre_entry.insert(0, item['values'][1])
            self.lab_estado_var.set(item['values'][2])
    
    def crear_laboratorio(self):
        """Crea un nuevo laboratorio"""
        nombre = self.lab_nombre_entry.get().strip()
        estado = self.lab_estado_var.get()
        
        success, message = self.admin_controller.crear_laboratorio(nombre, estado)
        if success:
            messagebox.showinfo("Éxito", message)
            self.lab_nombre_entry.delete(0, tk.END)
            self.cargar_laboratorios()
        else:
            messagebox.showerror("Error", message)
    
    def actualizar_laboratorio(self):
        """Actualiza un laboratorio seleccionado"""
        selection = self.lab_tree.selection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un laboratorio primero")
            return
        
        item = self.lab_tree.item(selection[0])
        lab_id = item['values'][0]
        nombre = self.lab_nombre_entry.get().strip()
        estado = self.lab_estado_var.get()
        
        success, message = self.admin_controller.actualizar_laboratorio(lab_id, nombre, estado)
        if success:
            messagebox.showinfo("Éxito", message)
            self.cargar_laboratorios()
        else:
            messagebox.showerror("Error", message)
    
    def eliminar_laboratorio(self):
        """Elimina un laboratorio seleccionado"""
        selection = self.lab_tree.selection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un laboratorio primero")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este laboratorio?"):
            item = self.lab_tree.item(selection[0])
            lab_id = item['values'][0]
            
            success, message = self.admin_controller.eliminar_laboratorio(lab_id)
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_laboratorios()
            else:
                messagebox.showerror("Error", message)
    
    def setup_usuarios_tab(self):
        """Configura la pestaña de usuarios"""
        # Frame de lista
        list_frame = tk.LabelFrame(self.tab_usuarios, text="Usuarios Registrados", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para usuarios
        columns = ('ID', 'Usuario', 'Rol', 'Fecha Registro')
        self.user_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=120)
        
        self.user_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.user_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botones
        btn_frame = tk.Frame(self.tab_usuarios, bg='#ecf0f1')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="Registrar Nuevo Usuario",
            command=self.abrir_registro,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Eliminar Seleccionado",
            command=self.eliminar_usuario,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        self.cargar_usuarios()
    
    def cargar_usuarios(self):
        """Carga la lista de usuarios"""
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        success, usuarios = self.auth_controller.get_usuarios()
        if success:
            for user in usuarios:
                self.user_tree.insert('', 'end', values=(
                    user['id'], 
                    user['username'], 
                    user['rol'], 
                    user['created_at']
                ))
    
    def abrir_registro(self):
        """Abre la ventana de registro de usuarios"""
        RegistroView(self.root, self.cargar_usuarios)
    
    def eliminar_usuario(self):
        """Elimina un usuario seleccionado"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un usuario primero")
            return
        
        item = self.user_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al usuario '{username}'?"):
            success, message = self.auth_controller.eliminar_usuario(user_id, self.user_data['id'])
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", message)
    
    def setup_inventario_tab(self):
        """Configura la pestaña de inventario"""
        # Frame de formulario
        form_frame = tk.LabelFrame(self.tab_inventario, text="Agregar Item", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        form_frame.pack(fill='x', padx=10, pady=10)
        
        form_inner = tk.Frame(form_frame, bg='#ecf0f1')
        form_inner.pack(padx=10, pady=10)
        
        # Laboratorio
        tk.Label(form_inner, text="Laboratorio:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        self.inv_lab_combo = ttk.Combobox(form_inner, state='readonly', width=37)
        self.inv_lab_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Nombre item
        tk.Label(form_inner, text="Nombre Item:", bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        self.inv_nombre_entry = tk.Entry(form_inner, width=40, font=('Arial', 10))
        self.inv_nombre_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Cantidad
        tk.Label(form_inner, text="Cantidad:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
        self.inv_cantidad_entry = tk.Entry(form_inner, width=40, font=('Arial', 10))
        self.inv_cantidad_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Botón
        tk.Button(
            form_inner,
            text="Agregar al Inventario",
            command=self.agregar_item,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Frame de lista
        list_frame = tk.LabelFrame(self.tab_inventario, text="Inventario Actual", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para inventario
        columns = ('ID', 'Laboratorio', 'Item', 'Cantidad')
        self.inv_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.inv_tree.heading(col, text=col)
            self.inv_tree.column(col, width=150)
        
        self.inv_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.inv_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.inv_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón eliminar
        tk.Button(
            list_frame,
            text="Eliminar Item",
            command=self.eliminar_item,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(pady=10)
        
        self.cargar_laboratorios_combo()
        self.cargar_inventario()
    
    def cargar_laboratorios_combo(self):
        """Carga laboratorios en el combobox de inventario"""
        success, laboratorios = self.admin_controller.obtener_laboratorios()
        if success:
            labs = [f"{lab['id']} - {lab['nombre']}" for lab in laboratorios]
            self.inv_lab_combo['values'] = labs
            if labs:
                self.inv_lab_combo.set(labs[0])
    
    def agregar_item(self):
        """Agrega un item al inventario"""
        lab_str = self.inv_lab_combo.get()
        if not lab_str:
            messagebox.showwarning("Atención", "Selecciona un laboratorio")
            return
        
        lab_id = int(lab_str.split(' - ')[0])
        nombre = self.inv_nombre_entry.get().strip()
        cantidad_str = self.inv_cantidad_entry.get().strip()
        
        if not nombre or not cantidad_str:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios")
            return
        
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
        
        success, message = self.admin_controller.agregar_item_inventario(lab_id, nombre, cantidad)
        if success:
            messagebox.showinfo("Éxito", message)
            self.inv_nombre_entry.delete(0, tk.END)
            self.inv_cantidad_entry.delete(0, tk.END)
            self.cargar_inventario()
        else:
            messagebox.showerror("Error", message)
    
    def cargar_inventario(self):
        """Carga el inventario en el treeview"""
        for item in self.inv_tree.get_children():
            self.inv_tree.delete(item)
        
        success, items = self.admin_controller.obtener_inventario()
        if success:
            for item in items:
                self.inv_tree.insert('', 'end', values=(
                    item['id'],
                    item['laboratorio_nombre'],
                    item['item_nombre'],
                    item['cantidad_total']
                ))
    
    def eliminar_item(self):
        """Elimina un item del inventario"""
        selection = self.inv_tree.selection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un item primero")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este item?"):
            item = self.inv_tree.item(selection[0])
            item_id = item['values'][0]
            
            success, message = self.admin_controller.eliminar_item_inventario(item_id)
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_inventario()
            else:
                messagebox.showerror("Error", message)
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cerrar sesión?"):
            self.root.destroy()
            self.logout_callback()