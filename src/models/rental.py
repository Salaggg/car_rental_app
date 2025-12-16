from datetime import datetime

class Rental:
    def __init__(self, rental_id, customer, vehicle, start_date, end_date):
        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True
        
        # calcul couts
        self.base_cost = self.calculate_base_cost()
        self.penalty_cost = 0 
    
    @property
    def total_cost(self):
        # prix base + penalité
        return self.base_cost + self.penalty_cost

    def calculate_base_cost(self):
        # calcul selon durée
        duration = self.end_date - self.start_date
        days = duration.days
        if days < 1: days = 1 
        return days * self.vehicle.daily_rate

    def add_penalty(self, amount, reason):
        # ajout frais sup
        self.penalty_cost += amount
        print(f"Pénalité de {amount}€ : {reason}")

    def end_rental(self):
        # fin location
        self.is_active = False
        self.vehicle.is_available = True