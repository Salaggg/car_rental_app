import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# import des classes
from src.services.rental_system import CarRentalSystem
from src.models.vehicle import Car, Truck, Motorcycle
from src.models.customer import Customer

class RentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agence de Location - Manager V3.0 (Final)")
        self.root.geometry("950x700") 

        # demarrage
        self.system = CarRentalSystem()
        self.setup_demo_data()

        # interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # fix pour mac
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

        # onglet 1 : parc
        self.tab_fleet = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_fleet, text="🚗 Parc Auto")
        self.create_fleet_view()

        # onglet 2 : louer
        self.tab_rent = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rent, text="📝 Louer")
        self.create_rental_form()

        # onglet 3 : retour (NOUVEAU)
        self.tab_return = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_return, text="↩️ Retour")
        self.create_return_view()

        # onglet 4 : admin
        self.tab_admin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_admin, text="➕ Admin")
        self.create_admin_view()
        
        self.refresh_list()

    def on_tab_change(self, event):
        self.refresh_list()

    def setup_demo_data(self):
        print("--- Chargement des données ---")
        self.system.add_vehicle(Car("V01", "Peugeot", "208", "Eco", 45))
        self.system.add_vehicle(Truck("T01", "Volvo", "FH16", "Lourd", 200, 5000))
        self.system.add_vehicle(Motorcycle("M01", "Yamaha", "MT-07", "Sport", 80, 700))

        self.system.add_customer(Customer(1, "Dupont", "Jean", 45, "B123"))
        self.system.add_customer(Customer(2, "Durand", "Kevin", 19, "B999"))

    # --- VUES ---

    def create_fleet_view(self):
        lbl = ttk.Label(self.tab_fleet, text="État de la flotte en temps réel", font=("Arial", 14))
        lbl.pack(pady=10)

        cols = ("Type", "Marque", "Modèle", "Prix/J", "Info", "État")
        self.tree = ttk.Treeview(self.tab_fleet, columns=cols, show='headings')
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110)

        self.tree.pack(pady=10, fill="both", expand=True, padx=10)
        
        ttk.Button(self.tab_fleet, text="Actualiser", command=self.refresh_list).pack(pady=10)

    def create_rental_form(self):
        frame = ttk.Frame(self.tab_rent)
        frame.pack(pady=10)

        ttk.Label(frame, text="1. Client :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_client = ttk.Combobox(frame, width=40, state="readonly") 
        self.combo_client.grid(row=1, column=0, padx=5, pady=0)

        ttk.Label(frame, text="2. Véhicule DISPO :").grid(row=2, column=0, sticky="w", padx=5, pady=(15, 5))
        
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=3, column=0)
        self.list_vehicles = tk.Listbox(list_frame, height=6, width=50)
        self.list_vehicles.pack(side="left", fill="y")
        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.list_vehicles.yview)
        sb.pack(side="right", fill="y")
        self.list_vehicles.config(yscrollcommand=sb.set)

        ttk.Label(frame, text="3. Durée (jours) :").grid(row=4, column=0, sticky="w", padx=5, pady=(15, 5))
        self.entry_days = ttk.Entry(frame, width=10)
        self.entry_days.grid(row=5, column=0, sticky="w", padx=5)

        ttk.Button(frame, text="✅ Valider la Location", command=self.process_rental).grid(row=6, column=0, pady=25)
        self.lbl_result = ttk.Label(frame, text="", foreground="blue")
        self.lbl_result.grid(row=7, column=0)

    def create_return_view(self):
        # onglet pour rendre la voiture et mettre penalité
        frame = ttk.Frame(self.tab_return)
        frame.pack(pady=20)

        ttk.Label(frame, text="Choisir le véhicule à rendre (actuellement loué) :").pack(anchor="w")
        
        # liste des vehicules loués
        list_frame = ttk.Frame(frame)
        list_frame.pack(pady=5)
        self.list_rented = tk.Listbox(list_frame, height=6, width=50)
        self.list_rented.pack(side="left", fill="y")
        
        ttk.Label(frame, text="Pénalité (€) (Optionnel : retard, dégats...) :").pack(anchor="w", pady=(15,5))
        self.entry_penalty = ttk.Entry(frame, width=10)
        self.entry_penalty.pack(anchor="w")
        self.entry_penalty.insert(0, "0") # 0 par defaut

        ttk.Button(frame, text="🔙 Valider le Retour", command=self.process_return).pack(pady=20)
        self.lbl_return_res = ttk.Label(frame, text="", foreground="blue")
        self.lbl_return_res.pack()

    def create_admin_view(self):
        main_frame = ttk.Frame(self.tab_admin)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # client
        f_cl = ttk.LabelFrame(main_frame, text="Ajouter Client"); f_cl.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Label(f_cl, text="Prénom:").pack(anchor="w"); self.e_fn = ttk.Entry(f_cl); self.e_fn.pack(fill="x")
        ttk.Label(f_cl, text="Nom:").pack(anchor="w"); self.e_ln = ttk.Entry(f_cl); self.e_ln.pack(fill="x")
        ttk.Label(f_cl, text="Age:").pack(anchor="w"); self.e_age = ttk.Entry(f_cl); self.e_age.pack(fill="x")
        ttk.Label(f_cl, text="Permis:").pack(anchor="w"); self.e_lic = ttk.Entry(f_cl); self.e_lic.pack(fill="x")
        ttk.Button(f_cl, text="Sauver Client", command=self.add_client).pack(pady=10)

        # vehicule
        f_ve = ttk.LabelFrame(main_frame, text="Ajouter Véhicule"); f_ve.pack(side="right", fill="both", expand=True, padx=5)
        ttk.Label(f_ve, text="Type:").pack(anchor="w")
        self.c_type = ttk.Combobox(f_ve, values=["Voiture", "Camion", "Moto"], state="readonly"); self.c_type.current(0); self.c_type.pack(fill="x")
        ttk.Label(f_ve, text="Marque:").pack(anchor="w"); self.e_br = ttk.Entry(f_ve); self.e_br.pack(fill="x")
        ttk.Label(f_ve, text="Modèle:").pack(anchor="w"); self.e_mo = ttk.Entry(f_ve); self.e_mo.pack(fill="x")
        ttk.Label(f_ve, text="Prix:").pack(anchor="w"); self.e_pr = ttk.Entry(f_ve); self.e_pr.pack(fill="x")
        ttk.Label(f_ve, text="Spec (CC/Kg):").pack(anchor="w"); self.e_sp = ttk.Entry(f_ve); self.e_sp.pack(fill="x")
        ttk.Button(f_ve, text="Sauver Véhicule", command=self.add_vehicle).pack(pady=10)

    # --- LOGIQUE ---

    def refresh_list(self):
        # 1. parc
        for row in self.tree.get_children(): self.tree.delete(row)
        for v in self.system.vehicles:
            etat = "DISPO" if v.is_available else "LOUE"
            if v.maintenance_due: etat = "MAINTENANCE"
            typ = "Voiture"
            if isinstance(v, Truck): typ="Camion"
            elif isinstance(v, Motorcycle): typ="Moto"
            self.tree.insert("", "end", values=(typ, v.brand, v.model, f"{v.daily_rate}€", "-", etat))

        # 2. clients
        cli = [f"{c.first_name} {c.last_name}" for c in self.system.customers]
        self.combo_client['values'] = cli
        
        # 3. vehicules dispo (pour louer)
        if hasattr(self, 'list_vehicles'):
            self.list_vehicles.delete(0, tk.END)
            dispos = self.system.report_available_vehicles()
            for v in dispos: self.list_vehicles.insert(tk.END, f"{v.brand} {v.model} - ID:{v.vehicle_id}")

        # 4. vehicules loués (pour retour)
        if hasattr(self, 'list_rented'):
            self.list_rented.delete(0, tk.END)
            loues = self.system.report_rented_vehicles()
            if not loues: self.list_rented.insert(tk.END, "--- Rien à rendre ---")
            for v in loues: self.list_rented.insert(tk.END, f"{v.brand} {v.model} - ID:{v.vehicle_id}")

    def process_rental(self):
        try:
            if self.combo_client.current() == -1: raise Exception("Client?")
            c = self.system.customers[self.combo_client.current()]
            
            sel = self.list_vehicles.curselection()
            if not sel: raise Exception("Véhicule?")
            vid = self.list_vehicles.get(sel[0]).split("ID:")[-1]
            v = next(v for v in self.system.vehicles if v.vehicle_id == vid)
            
            d = int(self.entry_days.get())
            start = datetime.now(); end = start + timedelta(days=d)
            
            r = self.system.rent_vehicle(c, v, start, end)
            
            messagebox.showinfo("OK", f"Loué! Coût estimé: {r.total_cost}€")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def process_return(self):
        try:
            sel = self.list_rented.curselection()
            if not sel: raise Exception("Sélectionner un véhicule à rendre")
            txt = self.list_rented.get(sel[0])
            if "---" in txt: return

            vid = txt.split("ID:")[-1]
            penal = float(self.entry_penalty.get())

            # appel au backend
            rental = self.system.return_vehicle(vid, penal)

            msg = f"Retour confirmé !\nPrix de base : {rental.base_cost}€\nPénalité : {rental.penalty_cost}€\nTOTAL FINAL : {rental.total_cost}€"
            messagebox.showinfo("Facture", msg)
            self.lbl_return_res.config(text=f"Dernier retour: {rental.total_cost}€", foreground="green")
            
            self.refresh_list()
            self.entry_penalty.delete(0, tk.END); self.entry_penalty.insert(0, "0")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def add_client(self):
        try:
            self.system.add_customer(Customer(len(self.system.customers)+1, self.e_fn.get(), self.e_ln.get(), int(self.e_age.get()), self.e_lic.get()))
            messagebox.showinfo("OK", "Client ajouté"); self.refresh_list()
        except: messagebox.showerror("Erreur", "Vérifier champs")

    def add_vehicle(self):
        try:
            t=self.c_type.get(); b=self.e_br.get(); m=self.e_mo.get(); p=float(self.e_pr.get()); s=int(self.e_sp.get())
            vid = f"{t[0]}{len(self.system.vehicles)+1:02d}"
            if t=="Voiture": v=Car(vid,b,m,"Std",p)
            elif t=="Camion": v=Truck(vid,b,m,"Hv",p,s)
            else: v=Motorcycle(vid,b,m,"Sp",p,s)
            self.system.add_vehicle(v)
            messagebox.showinfo("OK", "Véhicule ajouté"); self.refresh_list()
        except: messagebox.showerror("Erreur", "Vérifier champs")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try: style.theme_use('clam') 
    except: pass
    app = RentalApp(root)
    root.mainloop()