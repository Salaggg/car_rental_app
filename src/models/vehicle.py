from abc import ABC, abstractmethod

# classe parent (abstraite)
class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, model, category, daily_rate):
        # info de base
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.category = category
        self.daily_rate = daily_rate
        
        # etat du vehicule
        self.is_available = True
        self.maintenance_due = False

    def send_to_maintenance(self):
        # envoi au garage
        self.is_available = False
        self.maintenance_due = True

    def finish_maintenance(self):
        # retour du garage
        self.maintenance_due = False
        self.is_available = True

    @abstractmethod
    def get_type(self):
        pass

# classe voiture
class Car(Vehicle):
    def get_type(self):
        return "Voiture"

# classe camion
class Truck(Vehicle):
    def __init__(self, vehicle_id, brand, model, category, daily_rate, max_load):
        super().__init__(vehicle_id, brand, model, category, daily_rate)
        # charge max en kg
        self.max_load = max_load

    def get_type(self):
        return "Camion"

# classe moto
class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, brand, model, category, daily_rate, engine_cc):
        super().__init__(vehicle_id, brand, model, category, daily_rate)
        # cylindrée
        self.engine_cc = engine_cc

    def get_type(self):
        return "Moto"