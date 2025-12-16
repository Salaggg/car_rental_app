from src.services.rental_system import CarRentalSystem
from src.models.vehicle import Car, Truck
from src.models.customer import Customer
from datetime import datetime, timedelta

# script principal pour demo console

def main():
    print("--- DEMARRAGE AGENCE ---")
    sys = CarRentalSystem()

    # ajout flotte
    c1 = Car("V1", "Renault", "Clio", "Eco", 30)
    t1 = Truck("T1", "Volvo", "FH", "Lourd", 150, 2000)
    sys.add_vehicle(c1)
    sys.add_vehicle(t1)

    # ajout client
    client = Customer(1, "Thomas", "Test", 20, "B")
    sys.add_customer(client)

    # test location interdit (camion trop jeune)
    try:
        print("\nTentative location camion (20 ans)...")
        sys.rent_vehicle(client, t1, datetime.now(), datetime.now() + timedelta(days=1))
    except Exception as e:
        print(f"Erreur attrapée : {e}")

    # test location ok
    print("\nTentative location voiture...")
    sys.rent_vehicle(client, c1, datetime.now(), datetime.now() + timedelta(days=2))
    print("Location OK")

    # rapport
    print(f"\nCA Total : {sys.report_revenue()}€")

if __name__ == "__main__":
    main()