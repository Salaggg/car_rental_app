class Customer:
    def __init__(self, customer_id, first_name, last_name, age, license_number):
        # infos client
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.license_number = license_number
        
        # historique des locations
        self.rental_history = []

    def add_rental_to_history(self, rental):
        # ajout dans la liste
        self.rental_history.append(rental)