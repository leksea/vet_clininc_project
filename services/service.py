#-------------Service---------------
class Service:
    def __init__(self, name: str, specialty: str, experience: int, price:float):
        self._name = name
        self._specialty = specialty
        self._experience = experience
        self._price = price

    @property
    def name(self): return self._name
    @property
    def specialty(self): return self._specialty
    @property
    def experience(self): return self._experience
    @property
    def price(self): return self._price
    def __str__(self):
        return f"{self.name} | Specialty: {self.specialty} | Required Exp: {self.experience} yrs | Price: ${self.price:.2f}"
###########################TESTING##########################################
if __name__ == "__main__":
    print("--- Testing Service ---")
    services = [
        Service("Cat Neutering", "Surgery", 2, 95.00),
        Service("Dog Neutering", "Surgery", 3, 110.00),
        Service("Annual Exam - Cat", "Wellness", 1, 45.00),
        Service("Annual Exam - Dog", "Wellness", 1, 50.00),
        Service("Dental Cleaning", "Dental", 4, 150.00),
        Service("Orthopedic Surgery", "Orthopedic", 10, 1200.00),
        Service("Exotic Animal Checkup", "Exotics", 5, 90.00),
        Service("Reptile Heat Check", "Exotics", 2, 60.00),
        Service("Rabbit Nail Trim", "Grooming", 1, 15.00),
        Service("Chinchilla Fur Check", "Wellness", 2, 30.00)
    ]

    # Print all services
    print("Available Veterinary Services:")
    for svc in services:
        print(f" - {svc}")