import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.maestro_controller import MaestroController
from src.controllers.prestamo_controller import PrestamoController
from src.controllers.auth_controller import AuthController
from datetime import date
from tkcalendar import DateEntry

class MaestroView:
    def __init__(self, root, user_data, logout_callback):
        self.root = root
        self.root.title(f"Panel de Maestro - {user_data['username']}")
        self.root.geometry("950x650")
        self.root.configure(bg='#ecf0f1')
        
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.maestro_controller = MaestroController()
        self.maestro_controller.set_maestro(user_data)
        self.prestamo_controller = PrestamoController()
        self.prestamo_controller.set_usuario(user_data)
        self.auth_controller = AuthController()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del maestro"""
        # Barra superior
        top_bar = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_bar.pack(fill='x')
        
        tk.Label(
            top_bar,
            text=f"Bienvenido, {self.user_data['username']} (Maestro)",
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
        
        # Pestaña Reservar
        self.tab_reservar = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_reservar, text="📝 Reservar Laboratorio")
        
        # Pestaña Mis Reservas
        self.tab_mis_reservas = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_mis_reservas, text="📋 Mis Reservas")
        
        # Pestaña Préstamos
        self.tab_prestamos = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_prestamos, text="📦 Préstamos")
        
        # Pestaña Mi Cuenta
        self.tab_mi_cuenta = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.tab_mi_cuenta, text="🔑 Mi Cuenta")
        
        self.setup_reservar_tab()
        self.setup_mis_reservas_tab()
        self.setup_prestamos_tab()
        self.setup_mi_cuenta_tab()
    
    # ==================== RESERVAR LABORATORIO ====================
    def setup_reservar_tab(self):
        """Configura la pestaña de reservar"""
        main_frame = tk.Frame(self.tab_reservar, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="Nueva Reserva de Laboratorio",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        select_frame = tk.LabelFrame(main_frame, text="Seleccionar Laboratorio y Fecha", 
                                      bg='#ecf0f1', font=('Arial', 10, 'bold'))
        select_frame.pack(fill='x', pady=10)
        
        select_inner = tk.Frame(select_frame, bg='#ecf0f1')
        select_inner.pack(padx=20, pady=15)
        
        tk.Label(select_inner, text="Laboratorio:", font=('Arial', 11), bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        self.lab_combo = ttk.Combobox(select_inner, state='readonly', width=40, font=('Arial', 10))
        self.lab_combo.grid(row=0, column=1, padx=10, pady=5)
        self.lab_combo.bind('<<ComboboxSelected>>', self.cargar_bloques)
        
        tk.Label(select_inner, text="Fecha:", font=('Arial', 11), bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        self.fecha_entry = DateEntry(select_inner, width=40, font=('Arial', 10),
                                     date_pattern='yyyy-mm-dd', background='#2c3e50',
                                     foreground='white', borderwidth=2,
                                     mindate=date.today())
        self.fecha_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        tk.Button(
            select_inner,
            text="🔍 Ver Disponibilidad",
            command=self.cargar_bloques,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).grid(row=2, column=0, columnspan=2, pady=15)
        
        self.bloques_frame = tk.LabelFrame(main_frame, text="Bloques Horarios Disponibles", 
                                            bg='#ecf0f1', font=('Arial', 10, 'bold'))
        self.bloques_frame.pack(fill='both', expand=True, pady=10)
        
        self.cargar_laboratorios()
    
    def cargar_laboratorios(self):
        """Carga los laboratorios disponibles en el combobox"""
        success, laboratorios = self.maestro_controller.obtener_laboratorios_disponibles()
        if success:
            labs = [f"{lab['id']} - {lab['nombre']}" for lab in laboratorios]
            self.lab_combo['values'] = labs
            if labs:
                self.lab_combo.set(labs[0])
    
    def cargar_bloques(self, event=None):
        """Carga los bloques horarios disponibles"""
        for widget in self.bloques_frame.winfo_children():
            widget.destroy()
        
        lab_str = self.lab_combo.get()
        fecha = self.fecha_entry.get_date().strftime('%Y-%m-%d')
        
        if not lab_str or not fecha:
            messagebox.showwarning("Atención", "Selecciona laboratorio y fecha")
            return
        
        try:
            lab_id = int(lab_str.split(' - ')[0])
        except:
            messagebox.showerror("Error", "Selecciona un laboratorio válido")
            return
        
        success, bloques = self.maestro_controller.obtener_bloques_disponibles(lab_id, fecha)
        
        if not success:
            messagebox.showerror("Error", bloques if isinstance(bloques, str) else "Error al cargar bloques")
            return
        
        if not bloques:
            tk.Label(self.bloques_frame, text="No hay bloques disponibles para esta fecha",
                    font=('Arial', 11), bg='#ecf0f1', fg='#7f8c8d').pack(pady=30)
            return
        
        bloques_inner = tk.Frame(self.bloques_frame, bg='#ecf0f1')
        bloques_inner.pack(expand=True, padx=10, pady=10)
        
        for i, bloque in enumerate(bloques):
            row = i // 3
            col = i % 3
            
            if bloque['estado'] == 'disponible':
                btn = tk.Button(
                    bloques_inner,
                    text=f"🟢 {bloque['horario_mostrar']}\nDisponible",
                    command=lambda b=bloque: self.seleccionar_bloque(b),
                    bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'),
                    width=25, height=2, cursor='hand2', bd=0
                )
            else:
                btn = tk.Button(
                    bloques_inner,
                    text=f"🔴 {bloque['horario_mostrar']}\nOcupado",
                    state='disabled', bg='#e74c3c', fg='white',
                    font=('Arial', 10, 'bold'), width=25, height=2, bd=0
                )
            
            btn.grid(row=row, column=col, padx=5, pady=5)
    
    def seleccionar_bloque(self, bloque):
        """Maneja la selección de un bloque y crea la reserva"""
        lab_str = self.lab_combo.get()
        lab_id = int(lab_str.split(' - ')[0])
        fecha = self.fecha_entry.get_date().strftime('%Y-%m-%d')
        
        horas = bloque['horario_mostrar'].split(' - ')
        hora_inicio = horas[0]
        hora_fin = horas[1]
        
        if messagebox.askyesno("Confirmar Reserva",
                               f"¿Confirmas la reserva?\n\n"
                               f"Laboratorio: {lab_str.split(' - ')[1]}\n"
                               f"Fecha: {fecha}\n"
                               f"Horario: {bloque['horario_mostrar']}"):
            success, message = self.maestro_controller.crear_reserva(lab_id, fecha, hora_inicio, hora_fin)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_bloques()
            else:
                messagebox.showerror("Error", message)
    
    # ==================== MIS RESERVAS ====================
    def setup_mis_reservas_tab(self):
        """Configura la pestaña de mis reservas"""
        control_frame = tk.Frame(self.tab_mis_reservas, bg='#ecf0f1')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            control_frame, text="🔄 Actualizar", command=self.cargar_mis_reservas,
            bg='#3498db', fg='white', font=('Arial', 10), bd=0, padx=15, pady=5, cursor='hand2'
        ).pack(side='left')
        
        list_frame = tk.LabelFrame(self.tab_mis_reservas, text="Mis Reservas", 
                                    bg='#ecf0f1', font=('Arial', 10, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Laboratorio', 'Fecha', 'Horario', 'Estado')
        self.reserva_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.reserva_tree.heading(col, text=col)
            self.reserva_tree.column(col, width=120)
        
        self.reserva_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.reserva_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.reserva_tree.configure(yscrollcommand=scrollbar.set)
        
        tk.Button(
            self.tab_mis_reservas, text="Cancelar Reserva Seleccionada",
            command=self.cancelar_reserva, bg='#e74c3c', fg='white',
            font=('Arial', 10), bd=0, padx=15, pady=5, cursor='hand2'
        ).pack(pady=10)
        
        self.cargar_mis_reservas()
    
    def cargar_mis_reservas(self):
        """Carga las reservas del maestro"""
        for item in self.reserva_tree.get_children():
            self.reserva_tree.delete(item)
        
        success, reservas = self.maestro_controller.obtener_mis_reservas()
        if success:
            for reserva in reservas:
                estado_color = '✅' if reserva['estado'] == 'activa' else '❌'
                self.reserva_tree.insert('', 'end', values=(
                    reserva['id'], reserva['laboratorio'], reserva['fecha'],
                    reserva['horario_mostrar'], f"{estado_color} {reserva['estado']}"
                ))
    
    def cancelar_reserva(self):
        """Cancela una reserva seleccionada"""
        selection = self.reserva_tree.selection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona una reserva primero")
            return
        
        item = self.reserva_tree.item(selection[0])
        reserva_id = item['values'][0]
        estado = item['values'][4]
        
        if 'cancelada' in estado.lower():
            messagebox.showwarning("Atención", "Esta reserva ya está cancelada")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar esta reserva?"):
            success, message = self.maestro_controller.cancelar_mi_reserva(reserva_id)
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_mis_reservas()
            else:
                messagebox.showerror("Error", message)
    
    # ==================== PRÉSTAMOS ====================
    def setup_prestamos_tab(self):
        """Configura la pestaña de préstamos de inventario"""
        # Frame de solicitud
        solicitud_frame = tk.LabelFrame(self.tab_prestamos, text="Solicitar Préstamo de Material", 
                                         bg='#ecf0f1', font=('Arial', 10, 'bold'))
        solicitud_frame.pack(fill='x', padx=10, pady=10)
        
        solicitud_inner = tk.Frame(solicitud_frame, bg='#ecf0f1')
        solicitud_inner.pack(padx=20, pady=15)
        
        # 1. Seleccionar Laboratorio
        tk.Label(solicitud_inner, text="1. Seleccionar Laboratorio:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=(5, 2))
        self.prestamo_lab_combo = ttk.Combobox(solicitud_inner, state='readonly', width=60, font=('Arial', 10))
        self.prestamo_lab_combo.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky='ew')
        self.prestamo_lab_combo.bind('<<ComboboxSelected>>', self.on_lab_selected_prestamo)
        
        # 2. Seleccionar Item
        tk.Label(solicitud_inner, text="2. Seleccionar Item:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=2, column=0, sticky='w', pady=(5, 2))
        self.prestamo_item_combo = ttk.Combobox(solicitud_inner, state='readonly', width=60, font=('Arial', 10))
        self.prestamo_item_combo.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky='ew')
        self.prestamo_item_combo.bind('<<ComboboxSelected>>', self.on_item_selected_prestamo)
        
        # 3. Cantidad
        tk.Label(solicitud_inner, text="3. Cantidad a solicitar:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=4, column=0, sticky='w', pady=(5, 2))
        
        cantidad_frame = tk.Frame(solicitud_inner, bg='#ecf0f1')
        cantidad_frame.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky='w')
        
        self.prestamo_cantidad_entry = tk.Entry(cantidad_frame, width=15, font=('Arial', 12))
        self.prestamo_cantidad_entry.pack(side='left', padx=(0, 10))
        
        self.disponible_label = tk.Label(cantidad_frame, text="Disponibles: -", 
                                          font=('Arial', 10, 'bold'), bg='#ecf0f1', fg='#27ae60')
        self.disponible_label.pack(side='left')
        
        # 4. Botón solicitar
        tk.Button(
            solicitud_inner, text="📨 Enviar Solicitud de Préstamo",
            command=self.solicitar_prestamo, bg='#2980b9', fg='white',
            font=('Arial', 11, 'bold'), bd=0, padx=25, pady=10, cursor='hand2'
        ).grid(row=6, column=0, columnspan=2, pady=20)
        
        # Frame de mis solicitudes
        solicitudes_frame = tk.LabelFrame(self.tab_prestamos, text="Mis Solicitudes de Préstamo", 
                                           bg='#ecf0f1', font=('Arial', 10, 'bold'))
        solicitudes_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para solicitudes
        columns = ('ID', 'Laboratorio', 'Item', 'Cantidad', 'Estado', 'Fecha Solicitud', 'Respuesta')
        self.solicitudes_tree = ttk.Treeview(solicitudes_frame, columns=columns, show='headings', height=10)
        
        col_widths = {'ID': 40, 'Laboratorio': 120, 'Item': 120, 'Cantidad': 70, 
                      'Estado': 100, 'Fecha Solicitud': 140, 'Respuesta': 120}
        for col in columns:
            self.solicitudes_tree.heading(col, text=col)
            self.solicitudes_tree.column(col, width=col_widths[col])
        
        self.solicitudes_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(solicitudes_frame, orient='vertical', command=self.solicitudes_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.solicitudes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón actualizar
        tk.Button(
            self.tab_prestamos, text="🔄 Actualizar Lista",
            command=self.actualizar_todo_prestamos, bg='#95a5a6', fg='white',
            font=('Arial', 10), bd=0, padx=15, pady=5, cursor='hand2'
        ).pack(pady=5)
        
        # Cargar datos iniciales
        self.cargar_laboratorios_prestamo()
        self.cargar_mis_solicitudes()
    
    def cargar_laboratorios_prestamo(self):
        """Carga los laboratorios disponibles en el combobox de préstamos"""
        success, laboratorios = self.maestro_controller.obtener_laboratorios_disponibles()
        if success:
            labs = [f"ID:{lab['id']} - {lab['nombre']}" for lab in laboratorios]
            self.prestamo_lab_combo['values'] = labs
            if labs:
                self.prestamo_lab_combo.set('Selecciona un laboratorio...')
        else:
            self.prestamo_lab_combo['values'] = ['No hay laboratorios disponibles']
    
    def on_lab_selected_prestamo(self, event=None):
        """Cuando se selecciona un laboratorio, cargar sus items disponibles"""
        lab_str = self.prestamo_lab_combo.get()
        
        if not lab_str or lab_str.startswith('Selecciona') or 'No hay' in lab_str:
            self.prestamo_item_combo.set('Primero selecciona un laboratorio')
            self.prestamo_item_combo['values'] = []
            self.disponible_label.config(text="Disponibles: -")
            return
        
        try:
            lab_id = int(lab_str.split(' - ')[0].replace('ID:', ''))
        except:
            return
        
        # Limpiar
        self.prestamo_item_combo.set('Cargando items...')
        self.prestamo_cantidad_entry.delete(0, tk.END)
        self.disponible_label.config(text="Disponibles: -")
        
        # Obtener items disponibles
        success, items = self.prestamo_controller.obtener_inventario_disponible()
        
        if success:
            # Filtrar items por laboratorio seleccionado
            items_lab = [item for item in items if item['laboratorio_id'] == lab_id]
            
            if items_lab:
                items_list = []
                for item in items_lab:
                    items_list.append(
                        f"ID:{item['id']} - {item['item_nombre']} | Disponibles: {item['cantidad_disponible']}"
                    )
                self.prestamo_item_combo['values'] = items_list
                self.prestamo_item_combo.set('Selecciona un item...')
            else:
                self.prestamo_item_combo['values'] = ['No hay items disponibles en este laboratorio']
                self.prestamo_item_combo.set('No hay items disponibles en este laboratorio')
    
    def on_item_selected_prestamo(self, event=None):
        """Cuando se selecciona un item, mostrar cantidad disponible"""
        item_str = self.prestamo_item_combo.get()
        
        if not item_str or 'Selecciona' in item_str or 'No hay' in item_str:
            self.disponible_label.config(text="Disponibles: -")
            self.prestamo_cantidad_entry.delete(0, tk.END)
            return
        
        try:
            # Extraer cantidad disponible del formato "ID:5 - Nombre | Disponibles: 20"
            if 'Disponibles:' in item_str:
                disponible = int(item_str.split('Disponibles:')[1].strip())
                self.disponible_label.config(text=f"Disponibles: {disponible}")
                self.prestamo_cantidad_entry.delete(0, tk.END)
        except:
            self.disponible_label.config(text="Disponibles: -")
    
    def solicitar_prestamo(self):
        """Envía una solicitud de préstamo"""
        # Validar laboratorio
        lab_str = self.prestamo_lab_combo.get()
        if not lab_str or 'Selecciona' in lab_str or 'No hay' in lab_str:
            messagebox.showwarning("Atención", "Primero selecciona un laboratorio")
            self.prestamo_lab_combo.focus()
            return
        
        # Validar item
        item_str = self.prestamo_item_combo.get()
        if not item_str or 'Selecciona' in item_str or 'No hay' in item_str:
            messagebox.showwarning("Atención", "Selecciona un item del laboratorio")
            self.prestamo_item_combo.focus()
            return
        
        # Validar cantidad
        cantidad_str = self.prestamo_cantidad_entry.get().strip()
        if not cantidad_str:
            messagebox.showwarning("Atención", "Especifica la cantidad a solicitar")
            self.prestamo_cantidad_entry.focus()
            return
        
        try:
            # Extraer ID del formato "ID:5 - Nombre | Disponibles: 20"
            item_id = int(item_str.split(' - ')[0].replace('ID:', ''))
            cantidad = int(cantidad_str)
            
            # Extraer disponible
            disponible = 0
            if 'Disponibles:' in item_str:
                disponible = int(item_str.split('Disponibles:')[1].strip())
            
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero válido")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
            return
        
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return
        
        if cantidad > disponible:
            messagebox.showerror("Error", 
                f"No hay suficientes items disponibles.\n\n"
                f"Disponibles: {disponible}\n"
                f"Solicitado: {cantidad}\n\n"
                f"Por favor, reduce la cantidad.")
            return
        
        # Confirmar
        lab_nombre = lab_str.split(' - ')[1] if ' - ' in lab_str else lab_str
        item_nombre = item_str.split(' - ')[1].split('|')[0].strip() if ' - ' in item_str else item_str
        
        if messagebox.askyesno("Confirmar Solicitud",
                               f"¿Enviar solicitud de préstamo?\n\n"
                               f"👤 Profesor: {self.user_data['username']}\n"
                               f"🔬 Laboratorio: {lab_nombre}\n"
                               f"📦 Item: {item_nombre}\n"
                               f"🔢 Cantidad: {cantidad} de {disponible} disponibles"):
            success, message = self.prestamo_controller.solicitar_prestamo(item_id, cantidad)
            if success:
                messagebox.showinfo("Éxito", "✅ " + message)
                self.prestamo_cantidad_entry.delete(0, tk.END)
                # Recargar items del laboratorio seleccionado
                self.on_lab_selected_prestamo()
                self.cargar_mis_solicitudes()
            else:
                messagebox.showerror("Error", message)
    
    def cargar_mis_solicitudes(self):
        """Carga las solicitudes del maestro"""
        for item in self.solicitudes_tree.get_children():
            self.solicitudes_tree.delete(item)
        
        success, solicitudes = self.prestamo_controller.obtener_mis_solicitudes()
        if success:
            for sol in solicitudes:
                estado_emoji = '⏳ Pendiente' if sol['estado'] == 'pendiente' else \
                               '✅ Aprobada' if sol['estado'] == 'aprobada' else '❌ Rechazada'
                respuesta = sol.get('comentario', '') if sol['estado'] == 'rechazada' else \
                           sol.get('fecha_respuesta', 'Pendiente')
                
                self.solicitudes_tree.insert('', 'end', values=(
                    sol['id'], 
                    sol['laboratorio_nombre'], 
                    sol['item_nombre'],
                    sol['cantidad_solicitada'], 
                    estado_emoji,
                    sol['fecha_solicitud'], 
                    respuesta
                ))
    
    def actualizar_todo_prestamos(self):
        """Actualiza ambas listas de préstamos"""
        self.cargar_laboratorios_prestamo()
        self.on_lab_selected_prestamo()
        self.cargar_mis_solicitudes()
    
    # ==================== MI CUENTA ====================
    def setup_mi_cuenta_tab(self):
        """Configura la pestaña para cambiar contraseña propia del maestro"""
        frame = tk.Frame(self.tab_mi_cuenta, bg='#ecf0f1')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="Cambiar mi contraseña", font=('Arial', 14, 'bold'),
                 bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=0, columnspan=2, pady=(0, 20))

        labels = ["Contraseña actual:", "Nueva contraseña:", "Confirmar nueva contraseña:"]
        self.cuenta_entries = []
        for i, label in enumerate(labels):
            tk.Label(frame, text=label, bg='#ecf0f1', font=('Arial', 11)).grid(row=i+1, column=0, sticky='e', pady=8, padx=(0, 10))
            entry_frame = tk.Frame(frame, bg='#ecf0f1')
            entry_frame.grid(row=i+1, column=1, pady=8)
            entry = tk.Entry(entry_frame, show='•', font=('Arial', 11), width=25, bd=2, relief='groove')
            entry.pack(side='left')
            show_var = tk.BooleanVar(value=False)
            def make_toggle(e=entry, v=show_var):
                def toggle(): v.set(not v.get()); e.config(show='' if v.get() else '•')
                return toggle
            tk.Button(entry_frame, text='👁', command=make_toggle(), bg='#ecf0f1', bd=1, cursor='hand2').pack(side='left', padx=(5, 0))
            self.cuenta_entries.append(entry)

        tk.Button(
            frame, text="Guardar nueva contraseña", command=self.cambiar_mi_password,
            bg='#27ae60', fg='white', font=('Arial', 11), bd=0, padx=20, pady=8, cursor='hand2'
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def cambiar_mi_password(self):
        actual = self.cuenta_entries[0].get().strip()
        nueva = self.cuenta_entries[1].get().strip()
        confirmar = self.cuenta_entries[2].get().strip()

        if nueva != confirmar:
            messagebox.showerror("Error", "Las contraseñas nuevas no coinciden")
            return

        success, message = self.auth_controller.cambiar_password(self.user_data['id'], actual, nueva)
        if success:
            messagebox.showinfo("Éxito", message)
            for e in self.cuenta_entries:
                e.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)

    # ==================== CERRAR SESIÓN ====================
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cerrar sesión?"):
            self.root.destroy()
            self.logout_callback()