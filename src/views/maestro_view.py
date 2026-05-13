import tkinter as tk
from tkinter import messagebox, ttk
from controllers import MaestroController
from datetime import date

class MaestroView:
    def __init__(self, root, user_data, logout_callback):
        self.root = root
        self.root.title(f"Panel de Maestro - {user_data['username']}")
        self.root.geometry("900x600")
        self.root.configure(bg='#ecf0f1')
        
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.maestro_controller = MaestroController()
        self.maestro_controller.set_maestro(user_data)
        
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
        
        self.setup_reservar_tab()
        self.setup_mis_reservas_tab()
    
    def setup_reservar_tab(self):
        """Configura la pestaña de reservar"""
        # Frame principal
        main_frame = tk.Frame(self.tab_reservar, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="Nueva Reserva de Laboratorio",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        # Frame de selección
        select_frame = tk.LabelFrame(main_frame, text="Seleccionar Laboratorio y Fecha", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        select_frame.pack(fill='x', pady=10)
        
        select_inner = tk.Frame(select_frame, bg='#ecf0f1')
        select_inner.pack(padx=20, pady=15)
        
        # Laboratorio
        tk.Label(select_inner, text="Laboratorio:", font=('Arial', 11), bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        self.lab_combo = ttk.Combobox(select_inner, state='readonly', width=40, font=('Arial', 10))
        self.lab_combo.grid(row=0, column=1, padx=10, pady=5)
        self.lab_combo.bind('<<ComboboxSelected>>', self.cargar_bloques)
        
        # Fecha
        tk.Label(select_inner, text="Fecha:", font=('Arial', 11), bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        self.fecha_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        self.fecha_entry = tk.Entry(select_inner, textvariable=self.fecha_var, width=42, font=('Arial', 10))
        self.fecha_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Botón para cargar bloques
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
        
        # Frame de bloques horarios
        self.bloques_frame = tk.LabelFrame(main_frame, text="Bloques Horarios Disponibles", bg='#ecf0f1', font=('Arial', 10, 'bold'))
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
        # Limpiar frame de bloques
        for widget in self.bloques_frame.winfo_children():
            widget.destroy()
        
        lab_str = self.lab_combo.get()
        fecha = self.fecha_var.get().strip()
        
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
            if isinstance(bloques, str):
                messagebox.showerror("Error", bloques)
            else:
                messagebox.showerror("Error", "Error al cargar bloques")
            return
        
        if not bloques:
            tk.Label(
                self.bloques_frame,
                text="No hay bloques disponibles para esta fecha",
                font=('Arial', 11),
                bg='#ecf0f1',
                fg='#7f8c8d'
            ).pack(pady=30)
            return
        
        # Frame para los botones de bloques
        bloques_inner = tk.Frame(self.bloques_frame, bg='#ecf0f1')
        bloques_inner.pack(expand=True, padx=10, pady=10)
        
        # Crear botones para cada bloque (en grid)
        for i, bloque in enumerate(bloques):
            row = i // 3
            col = i % 3
            
            if bloque['estado'] == 'disponible':
                btn = tk.Button(
                    bloques_inner,
                    text=f"🟢 {bloque['horario_mostrar']}\nDisponible",
                    command=lambda b=bloque: self.seleccionar_bloque(b),
                    bg='#2ecc71',
                    fg='white',
                    font=('Arial', 10, 'bold'),
                    width=25,
                    height=2,
                    cursor='hand2',
                    bd=0
                )
            else:
                btn = tk.Button(
                    bloques_inner,
                    text=f"🔴 {bloque['horario_mostrar']}\nOcupado",
                    state='disabled',
                    bg='#e74c3c',
                    fg='white',
                    font=('Arial', 10, 'bold'),
                    width=25,
                    height=2,
                    bd=0
                )
            
            btn.grid(row=row, column=col, padx=5, pady=5)
    
    def seleccionar_bloque(self, bloque):
        """Maneja la selección de un bloque y crea la reserva"""
        lab_str = self.lab_combo.get()
        lab_id = int(lab_str.split(' - ')[0])
        fecha = self.fecha_var.get().strip()
        
        # Extraer horas del horario_mostrar
        horas = bloque['horario_mostrar'].split(' - ')
        hora_inicio = horas[0]
        hora_fin = horas[1]
        
        # Confirmar reserva
        if messagebox.askyesno(
            "Confirmar Reserva",
            f"¿Confirmas la reserva?\n\n"
            f"Laboratorio: {lab_str.split(' - ')[1]}\n"
            f"Fecha: {fecha}\n"
            f"Horario: {bloque['horario_mostrar']}"
        ):
            success, message = self.maestro_controller.crear_reserva(
                lab_id, fecha, hora_inicio, hora_fin
            )
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.cargar_bloques()  # Recargar bloques
            else:
                messagebox.showerror("Error", message)
    
    def setup_mis_reservas_tab(self):
        """Configura la pestaña de mis reservas"""
        # Frame de control
        control_frame = tk.Frame(self.tab_mis_reservas, bg='#ecf0f1')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            control_frame,
            text="🔄 Actualizar",
            command=self.cargar_mis_reservas,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left')
        
        # Frame de lista
        list_frame = tk.LabelFrame(self.tab_mis_reservas, text="Mis Reservas", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para reservas
        columns = ('ID', 'Laboratorio', 'Fecha', 'Horario', 'Estado')
        self.reserva_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.reserva_tree.heading(col, text=col)
            self.reserva_tree.column(col, width=120)
        
        self.reserva_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.reserva_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.reserva_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón cancelar
        tk.Button(
            self.tab_mis_reservas,
            text="Cancelar Reserva Seleccionada",
            command=self.cancelar_reserva,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
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
                    reserva['id'],
                    reserva['laboratorio'],
                    reserva['fecha'],
                    reserva['horario_mostrar'],
                    f"{estado_color} {reserva['estado']}"
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
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cerrar sesión?"):
            self.root.destroy()
            self.logout_callback()