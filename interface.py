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

        # fix pour mac (clic onglet)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

        # onglets
        self.tab_fleet = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_fleet, text="🚗 Parc Automobile")
        self.create_fleet_view()

        self.tab_rent = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rent, text="📝 Nouvelle Location")
        self.create_rental_form()

        # admin
        self.tab_admin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_admin, text="➕ Administration")
        self.create_admin_view()
        
        self.refresh_list()

    def on_tab_change(self, event):
        # refresh au clic
        self.refresh_list()

    def setup_demo_data(self):
        # fausses données
        print("--- Chargement des données ---")
        self.system.add_vehicle(Car("V01", "Peugeot", "208", "Eco", 45))
        self.system.add_vehicle(Truck("T01", "Volvo", "FH16", "Lourd", 200, 5000))
        self.system.add_vehicle(Motorcycle("M01", "Yamaha", "MT-07", "Sport", 80, 700))

        self.system.add_customer(Customer(1, "Dupont", "Jean", 45, "B123"))
        self.system.add_customer(Customer(2, "Durand", "Kevin", 19, "B999"))

    def create_fleet_view(self):
        lbl = ttk.Label(self.tab_fleet, text="État de la flotte en temps réel", font=("Arial", 14))
        lbl.pack(pady=10)

        # colonnes
        cols = ("Type", "Marque", "Modèle", "Prix/J", "Info", "État")
        self.tree = ttk.Treeview(self.tab_fleet, columns=cols, show='headings')
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110)

        self.tree.pack(pady=10, fill="both", expand=True, padx=10)
        
        # bouton refresh
        ttk.Button(self.tab_fleet, text="Actualiser la liste", command=self.refresh_list).pack(pady=10)

    def create_rental_form(self):
        frame = ttk.Frame(self.tab_rent)
        frame.pack(pady=10)

        # liste des clients
        ttk.Label(frame, text="1. Choisir le Client :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_client = ttk.Combobox(frame, width=40, state="readonly") 
        self.combo_client.grid(row=1, column=0, padx=5, pady=0)

        # liste vehicule
        ttk.Label(frame, text="2. Choisir un Véhicule DISPONIBLE :").grid(row=2, column=0, sticky="w", padx=5, pady=(15, 5))
        
        # cadre liste
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=3, column=0)
        
        self.list_vehicles = tk.Listbox(list_frame, height=8, width=50, selectmode='SINGLE')
        self.list_vehicles.pack(side="left", fill="y")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.list_vehicles.yview)
        scrollbar.pack(side="right", fill="y")
        self.list_vehicles.config(yscrollcommand=scrollbar.set)

        # durée location
        ttk.Label(frame, text="3. Durée (jours) :").grid(row=4, column=0, sticky="w", padx=5, pady=(15, 5))
        self.entry_days = ttk.Entry(frame, width=10)
        self.entry_days.grid(row=5, column=0, sticky="w", padx=5)

        # bouton valider
        btn_action = ttk.Button(frame, text="✅ Valider la Location", command=self.process_rental)
        btn_action.grid(row=6, column=0, pady=25)

        # resultat
        self.lbl_result = ttk.Label(frame, text="", foreground="blue", font=("Arial", 11, "bold"))
        self.lbl_result.grid(row=7, column=0)

    def create_admin_view(self):
        main_frame = ttk.Frame(self.tab_admin)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ajout client
        frame_client = ttk.LabelFrame(main_frame, text=" Ajouter un Client ")
        frame_client.pack(side="left", fill="both", expand=True, padx=10)

        ttk.Label(frame_client, text="Prénom :").pack(anchor="w", padx=5)
        self.entry_c_first = ttk.Entry(frame_client); self.entry_c_first.pack(fill="x", padx=5)

        ttk.Label(frame_client, text="Nom :").pack(anchor="w", padx=5)
        self.entry_c_last = ttk.Entry(frame_client); self.entry_c_last.pack(fill="x", padx=5)

        ttk.Label(frame_client, text="Âge :").pack(anchor="w", padx=5)
        self.entry_c_age = ttk.Entry(frame_client); self.entry_c_age.pack(fill="x", padx=5)

        ttk.Label(frame_client, text="Permis (ex: B) :").pack(anchor="w", padx=5)
        self.entry_c_lic = ttk.Entry(frame_client); self.entry_c_lic.pack(fill="x", padx=5)

        # bouton save client
        ttk.Button(frame_client, text="💾 Sauvegarder Client", command=self.action_add_client).pack(pady=20)

        # ajout vehicule
        frame_veh = ttk.LabelFrame(main_frame, text=" Ajouter un Véhicule ")
        frame_veh.pack(side="right", fill="both", expand=True, padx=10)

        ttk.Label(frame_veh, text="Type :").pack(anchor="w", padx=5)
        self.combo_v_type = ttk.Combobox(frame_veh, values=["Voiture", "Camion", "Moto"], state="readonly")
        self.combo_v_type.current(0)
        self.combo_v_type.pack(fill="x", padx=5)

        ttk.Label(frame_veh, text="Marque :").pack(anchor="w", padx=5)
        self.entry_v_brand = ttk.Entry(frame_veh); self.entry_v_brand.pack(fill="x", padx=5)

        ttk.Label(frame_veh, text="Modèle :").pack(anchor="w", padx=5)
        self.entry_v_model = ttk.Entry(frame_veh); self.entry_v_model.pack(fill="x", padx=5)

        ttk.Label(frame_veh, text="Prix / Jour (€) :").pack(anchor="w", padx=5)
        self.entry_v_price = ttk.Entry(frame_veh); self.entry_v_price.pack(fill="x", padx=5)

        ttk.Label(frame_veh, text="Spécifique (CC ou Charge) :").pack(anchor="w", padx=5)
        self.entry_v_spec = ttk.Entry(frame_veh); self.entry_v_spec.pack(fill="x", padx=5)

        # bouton save vehicule
        ttk.Button(frame_veh, text="💾 Sauvegarder Véhicule", command=self.action_add_vehicle).pack(pady=20)

    def refresh_list(self):
        # update tableau 
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for v in self.system.vehicles:
            etat = "DISPO" if v.is_available else "LOUE"
            if v.maintenance_due: etat = "MAINTENANCE"
            
            # affichage
            type_v = "Voiture"
            info = "-"
            if isinstance(v, Truck): 
                type_v = "Camion"
                info = f"{v.max_load}kg"
            elif isinstance(v, Motorcycle): 
                type_v = "Moto"
                info = f"{v.engine_cc}cc"

            self.tree.insert("", "end", values=(type_v, v.brand, v.model, f"{v.daily_rate}€", info, etat))
        
        # update liste clients
        clients = [f"{c.first_name} {c.last_name} ({c.age} ans)" for c in self.system.customers]
        self.combo_client['values'] = clients
        
        # update liste vehicule
        if hasattr(self, 'list_vehicles'):
            self.list_vehicles.delete(0, tk.END) 
            dispos = self.system.report_available_vehicles()
            
            if not dispos:
                self.list_vehicles.insert(tk.END, "--- AUCUN VÉHICULE DISPONIBLE ---")
            else:
                for v in dispos:
                    self.list_vehicles.insert(tk.END, f"[{v.brand} {v.model}] - {v.daily_rate}€/j - ID:{v.vehicle_id}")

    def action_add_client(self):
        try:
            fn = self.entry_c_first.get()
            ln = self.entry_c_last.get()
            age = int(self.entry_c_age.get())
            lic = self.entry_c_lic.get()
            
            if not fn or not ln: raise Exception("Nom incomplet")

            new_id = len(self.system.customers) + 1
            new_c = Customer(new_id, fn, ln, age, lic)
            self.system.add_customer(new_c)
            
            messagebox.showinfo("OK", f"Client {fn} ajouté !")
            self.refresh_list()
            
            # clean
            self.entry_c_first.delete(0, tk.END)
            self.entry_c_last.delete(0, tk.END)
            self.entry_c_age.delete(0, tk.END)
            self.entry_c_lic.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur saisie : {e}")

    def action_add_vehicle(self):
        try:
            v_type = self.combo_v_type.get()
            brand = self.entry_v_brand.get()
            model = self.entry_v_model.get()
            price = float(self.entry_v_price.get())
            spec = self.entry_v_spec.get() 

            # id auto
            v_id = f"{v_type[0]}{len(self.system.vehicles)+1:02d}" 

            if v_type == "Voiture":
                new_v = Car(v_id, brand, model, "Standard", price)
            elif v_type == "Camion":
                new_v = Truck(v_id, brand, model, "Lourd", price, int(spec))
            elif v_type == "Moto":
                new_v = Motorcycle(v_id, brand, model, "Sport", price, int(spec))
            
            self.system.add_vehicle(new_v)
            messagebox.showinfo("OK", f"{v_type} {brand} ajouté !")
            self.refresh_list()
            
            # clean
            self.entry_v_brand.delete(0, tk.END)
            self.entry_v_model.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erreur", f"Vérifiez les valeurs. \n{e}")

    def process_rental(self):
        try:
            # recup client
            if self.combo_client.current() == -1:
                raise Exception("Sélectionnez un client.")
            customer_obj = self.system.customers[self.combo_client.current()]

            # recup vehicule
            selection = self.list_vehicles.curselection()
            if not selection:
                raise Exception("Veuillez cliquer sur un véhicule dans la liste.")
            
            text_line = self.list_vehicles.get(selection[0])
            if "---" in text_line:
                raise Exception("Aucun véhicule disponible.")

            # extraction id
            v_id = text_line.split("ID:")[-1]
            vehicle_obj = next((v for v in self.system.vehicles if v.vehicle_id == v_id), None)

            # duree
            days_str = self.entry_days.get()
            if not days_str.isdigit() or int(days_str) <= 0:
                raise Exception("Durée invalide (entrez un chiffre > 0).")
            
            days = int(days_str)
            start = datetime.now()
            end = start + timedelta(days=days)

            # backend
            rental = self.system.rent_vehicle(customer_obj, vehicle_obj, start, end)

            # succes
            msg = f"✅ Location validée !\nVéhicule : {vehicle_obj.brand} {vehicle_obj.model}\nCoût total : {rental.total_cost}€"
            messagebox.showinfo("Succès", msg)
            self.lbl_result.config(text=f"Dernière action : Location OK ({rental.total_cost}€)", foreground="green")

            # reset
            self.refresh_list()
            self.entry_days.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            self.lbl_result.config(text=f"Erreur : {e}", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try: style.theme_use('clam') 
    except: pass
    app = RentalApp(root)
    root.mainloop()