from src.models.rental import Rental
from src.models.vehicle import Car, Truck, Motorcycle

class CarRentalSystem:
    def __init__(self):
        # listes de données
        self.vehicles = []
        self.customers = []
        self.rentals = []

    # gestion vehicules
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def find_vehicle(self, brand=None, category=None):
        results = []
        for v in self.vehicles:
            if brand and v.brand.lower() != brand.lower():
                continue
            if category and v.category.lower() != category.lower():
                continue
            results.append(v)
        return results

    # gestion clients
    def add_customer(self, customer):
        self.customers.append(customer)
        print(f"Client ajouté : {customer.first_name}")

    def find_customer(self, name):
        return [c for c in self.customers if c.last_name.lower() == name.lower()]

    # location (départ)
    def rent_vehicle(self, customer, vehicle, start_date, end_date):
        # 0. verif dates
        if end_date < start_date:
            raise Exception("Erreur date : fin avant debut")

        # 1. verif dispo
        if not vehicle.is_available:
            raise Exception(f"Vehicule {vehicle.brand} pas dispo")
        
        if vehicle.maintenance_due:
            raise Exception("Vehicule en maintenance")

        # 2. verif age
        if customer.age < 18:
            raise Exception("Client mineur")
        if isinstance(vehicle, Motorcycle) and customer.age < 20:
            raise Exception("Faut 20 ans pour moto")
        if isinstance(vehicle, Truck) and customer.age < 25:
            raise Exception("Faut 25 ans pour camion")

        # 3. creation location
        rental_id = len(self.rentals) + 1
        new_rental = Rental(rental_id, customer, vehicle, start_date, end_date)
        
        # 4. update etats
        vehicle.is_available = False
        self.rentals.append(new_rental)
        customer.add_rental_to_history(new_rental)
        
        return new_rental

    # GESTION DU RETOUR ET PENALITE 
    def return_vehicle(self, vehicle_id, penalty_amount=0):
        # 1. trouver le véhicule
        vehicle = next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
        if not vehicle:
            raise Exception("Véhicule introuvable")

        # trouver la location active pour ce véhicule
        # on cherche dans les locations qui sont encore actives (is_active = True)
        active_rental = next((r for r in self.rentals if r.vehicle == vehicle and r.is_active), None)
        
        if not active_rental:
            raise Exception("Ce véhicule n'est pas loué actuellement.")

        # 3. appliquer pénalité
        if penalty_amount > 0:
            active_rental.add_penalty(penalty_amount, "Pénalité au retour")

        # 4. finir la location (rend la voiture dispo)
        active_rental.end_rental()
        
        return active_rental

    # rapports
    def report_available_vehicles(self):
        return [v for v in self.vehicles if v.is_available]
    
    def report_rented_vehicles(self):
        # pour la liste des retours
        return [v for v in self.vehicles if not v.is_available and not v.maintenance_due]

    def report_revenue(self):
        return sum(r.total_cost for r in self.rentals)