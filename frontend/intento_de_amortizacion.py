import customtkinter as ctk

class SimuladorFinanciamiento(ctk.CTkToplevel):
    def __init__(self, master=None, precio_fijo=150000, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Simulación de Amortización")
        self.geometry("500x650")
        
        self.precio = float(precio_fijo)
        self.meses = 12 
        

        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(self.frame_controles, text="Plazo de Financiamiento:").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.menu_meses = ctk.CTkOptionMenu(
            self.frame_controles, 
            values=["12", "24", "48"], 
            command=self.cambiar_plazo
        )
        self.menu_meses.set(str(self.meses))
        self.menu_meses.grid(row=0, column=1, padx=15, pady=15)
        
        self.scroll_container = ctk.CTkScrollableFrame(self)
        self.scroll_container.place(relx=0.04, rely=0.18, relwidth=0.92, relheight=0.78)
        
        
        self.tabla()

    def cambiar_plazo(self, seleccion):
        self.meses = int(seleccion)
        self.tabla()

    def tabla(self):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        
        enganche = self.precio * 0.10
        monto = self.precio - enganche
        tasa = 0.12
        
        total_con_intereses = monto * (1 + self.meses * (tasa / 12))
        monto_individual = total_con_intereses / self.meses
        suma_monto_y_total = monto + total_con_intereses
        
        
        frame_encabezado = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        frame_encabezado.pack(fill="x", padx=10, pady=(5, 10))
        
        lbl_mes_hdr = ctk.CTkLabel(frame_encabezado, text="Mes", font=ctk.CTkFont(weight="bold"))
        lbl_mes_hdr.pack(side="left", padx=5)
        
        lbl_monto_hdr = ctk.CTkLabel(frame_encabezado, text="Monto Individual", font=ctk.CTkFont(weight="bold"))
        lbl_monto_hdr.pack(side="right", padx=5)
        
        
        for mes in range(1, self.meses + 1):
            frame_fila = ctk.CTkFrame(self.scroll_container)
            frame_fila.pack(fill="x", padx=10, pady=4)
            
            lbl_mes = ctk.CTkLabel(frame_fila, text=f"Mes {mes}")
            lbl_mes.pack(side="left", padx=15, pady=5)
            
            lbl_monto = ctk.CTkLabel(frame_fila, text=f"${monto_individual:,.2f}")
            lbl_monto.pack(side="right", padx=15, pady=5)
            
        frame_espacio = ctk.CTkFrame(self.scroll_container, fg_color="transparent", height=20)
        frame_espacio.pack(fill="x", pady=5)
        
        
        frame_totales = ctk.CTkFrame(self.scroll_container, fg_color="transparent", border_width=1, border_color="gray")
        frame_totales.pack(fill="x", padx=10, pady=10)
        
        f_monto = ctk.CTkFrame(frame_totales, fg_color="transparent")
        f_monto.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(f_monto, text="Monto Neto Financiado:", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(f_monto, text=f"${monto:,.2f}", font=ctk.CTkFont(size=12)).pack(side="right")
        
        f_total = ctk.CTkFrame(frame_totales, fg_color="transparent")
        f_total.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(f_total, text="Total con Intereses:", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(f_total, text=f"${total_con_intereses:,.2f}", font=ctk.CTkFont(size=12)).pack(side="right")
        
        
        lbl_linea = ctk.CTkLabel(frame_totales, text="—" * 40, text_color="gray")
        lbl_linea.pack(fill="x", pady=2)
        
        
        f_suma_final = ctk.CTkFrame(frame_totales, fg_color="transparent")
        f_suma_final.pack(fill="x", padx=10, pady=(2, 6))
        ctk.CTkLabel(f_suma_final, text="Suma Total Combinada:", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkLabel(f_suma_final, text=f"${suma_monto_y_total:,.2f}", font=ctk.CTkFont(size=13, weight="bold")).pack(side="right")
