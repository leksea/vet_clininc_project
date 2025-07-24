from typing import List
import random as rd
import string
from models.petowner import PetOwner
from models.pet import Pet

class Client:
    def __init__(self, pet_owner: PetOwner, pet: Pet, primary_vet_id: str):
        self.client_id = self.generate_client_id()
        self.pet = pet
        self.owner_name = pet_owner.name.strip()
        self.phone_number = pet_owner._phone
        self.email = pet_owner._email
        self.primary_vet_id = primary_vet_id
        self._pet_owner = pet_owner

        self.firstname = pet.name
        self.lastname = self.extract_lastname(self.owner_name)
        self.dob = pet.age
        self.type = pet.type
        self.breed = pet.breed

        self.medical_history: List[str] = []
        self.billing_history: List[str] = []
        self.appointments: List["Appointment"] = []


    def generate_client_id(self) -> str:
        return ''.join(rd.choices(string.ascii_letters + string.digits, k=6))

    def extract_lastname(self, full_name: str) -> str:
        return full_name.split()[-1] if full_name else ""

    def add_appointment(self, appointment: "Appointment"):
        self.appointments.append(appointment)
        self._pet_owner._appointments.append(appointment)

    def remove_appointment(self, appointment: "Appointment"):
        if appointment in self.appointments:
            self.appointments.remove(appointment)
            self._pet_owner._appointments.remove(appointment)

    def add_medical_record(self, record: str):
        self.medical_history.append(record)

    def add_billing_record(self, entry: str):
        self.billing_history.append(entry)

    def __str__(self):
        return (f"Client {self.firstname} (Owner: {self.owner_name}) | "
                f"Type: {self.type}, Breed: {self.breed}, Phone: {self.phone_number}")

###########################TESTING##########################################
if __name__ == "__main__":
    print("--- Testing Client ---")
    from datetime import date

    class TestPet:
        def __init__(self):
            self.name = "Bruno"
            self.age = date(2020, 6, 10)
            self.type = "Dog"
            self.breed = "Labradoodle"

    class TestPetOwner:
        def __init__(self):
            self.name = "John Doe"
            self._phone = "555-1234"
            self._email = "john@yahoo.com"

    # Create instances
    pet = TestPet()
    owner = TestPetOwner()

    # Create client
    client = Client(pet_owner=owner, pet=pet, primary_vet_id="Vet123")

    # Test string representation
    print(client)

    # Add records
    client.add_medical_record("Rabies vaccination - 2024-01-10")
    client.add_billing_record("Invoice #001 - $85.00")

    # Print lists to verify
    print("Medical History:", client.medical_history)
    print("Billing History:", client.billing_history)

    # Simulate dummy appointment
    class DummyAppointment:
        def __str__(self): return "Dummy Appointment 1"

    client.add_appointment(DummyAppointment())
    print("Appointments:", [str(a) for a in client.appointments])