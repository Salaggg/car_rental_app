import unittest
from datetime import datetime, timedelta
from src.services.rental_system import CarRentalSystem
from src.models.vehicle import Car, Truck, Motorcycle
from src.models.customer import Customer

class TestRentalSystem(unittest.TestCase):
    
    def setUp(self):
        # demarrage avant chaque test
        self.system = CarRentalSystem()
        
        # ajout vehicules
        self.car = Car("V1", "Peugeot", "208", "Citadine", 50)
        self.truck = Truck("T1", "Volvo", "FH", "Lourd", 200, 5000)
        self.moto = Motorcycle("M1", "Yamaha", "MT07", "Roadster", 80, 700)
        
        self.system.add_vehicle(self.car)
        self.system.add_vehicle(self.truck)
        self.system.add_vehicle(self.moto)
        
        # ajout clients
        self.adult = Customer(1, "Jean", "Adulte", 30, "B1") 
        self.young = Customer(2, "Kevin", "Jeune", 19, "B2")      
        
        self.system.add_customer(self.adult)
        self.system.add_customer(self.young)

    # tests simples
    def test_search_vehicle(self):
        # verif recherche
        results = self.system.find_vehicle(brand="Peugeot")
        self.assertEqual(len(results), 1)

    def test_rent_vehicle_success(self):
        # cas normal location
        start = datetime.now()
        end = start + timedelta(days=3)
        
        rental = self.system.rent_vehicle(self.adult, self.car, start, end)
        
        # verif si plus dispo
        self.assertFalse(self.car.is_available)
        # verif prix (50 * 3)
        self.assertEqual(rental.total_cost, 150)

    # tests age
    def test_rent_truck_age_restriction(self):
        # jeune 19 ans veut camion -> erreur
        start = datetime.now()
        end = start + timedelta(days=1)
        
        with self.assertRaises(Exception) as context:
            self.system.rent_vehicle(self.young, self.truck, start, end)
        
        self.assertTrue("25 ans" in str(context.exception))

    def test_rent_moto_age_restriction(self):
        # jeune 19 ans veut moto -> erreur
        start = datetime.now()
        end = start + timedelta(days=1)
        
        with self.assertRaises(Exception) as context:
            self.system.rent_vehicle(self.young, self.moto, start, end)

    # tests pannes
    def test_rent_unavailable_vehicle(self):
        # deja loué
        start = datetime.now()
        end = start + timedelta(days=1)
        
        self.system.rent_vehicle(self.adult, self.car, start, end)
        
        # on re-loue la meme -> bug
        with self.assertRaises(Exception):
            self.system.rent_vehicle(self.adult, self.car, start, end)

    def test_rent_maintenance_vehicle(self):
        # vehicule au garage
        self.car.send_to_maintenance()
        
        start = datetime.now()
        end = start + timedelta(days=1)
        
        with self.assertRaises(Exception):
            self.system.rent_vehicle(self.adult, self.car, start, end)

    # tests dates
    def test_invalid_dates(self):
        # retour dans le passé
        start = datetime.now()
        end = start - timedelta(days=1) 
        
        with self.assertRaises(Exception):
            self.system.rent_vehicle(self.adult, self.car, start, end)

    # tests finance
    def test_revenue_report(self):
        # verif chiffre affaire global
        start = datetime.now()
        end = start + timedelta(days=2) 
        
        # 2 locs
        self.system.rent_vehicle(self.adult, self.car, start, end)
        self.system.rent_vehicle(self.adult, self.truck, start, end)
        
        # total 100 + 400 = 500
        total = self.system.report_revenue()
        self.assertEqual(total, 500)

if __name__ == '__main__':
    unittest.main()