from models.human import Human
from models.pet import Pet
from models.animals import Animal, DietType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.vetclinic import VetClinic
    from services.appointment import Appointment

from datetime import date, datetime
# ----------------- Pet Owner  -----------------
class PetOwner(Human):
    def __init__(self, name, dob, sex, race, weight, height, diet=DietType.OMNIVORE,
                 phone: str = "", email: str = ""):
        super().__init__(name, dob, sex, race, weight, height, diet)
        self._phone = phone
        self._email = email
        self._pets: list[Pet] = []
        self._vets: list["VetClininc"] = []
        self._appointments:list["Appointment"] = []

    def add_pet(self, animal: Animal, microchipped=False, neutered_or_sprayed=False):
        pet = Pet(animal, self, microchipped, neutered_or_sprayed)
        self._pets.append(pet)
        return pet

    def remove_pet(self, pet: Pet):
        if pet in self._pets:
            self._pets.remove(pet)

    def get_pets(self):
        return self._pets

    def get_contact_info(self):
        return f"{self._phone} | {self._email}"

    def list_pets(self):
        return [str(pet) for pet in self._pets]

    def __str__(self):
        return f"{self.name}, Pet Owner of {len(self._pets)} pet(s)"

    # --- Pet Management Methods ---
    def add_vet_clinic(self, clinic: "VetClinic"):
        if clinic not in self._vet_clinics:
            self._vet_clinics.append(clinic)
            print(f"{self.name} is now registered with {clinic._name}.")
        else:
            print(f"{self.name} is already registered with {clinic._name}.")

    def list_vet_clinics(self):
        return [c._name for c in self._vet_clinics]

    # --- Appointment System ---
    def make_appointment(self, clinic: "VetClinic", pet_name: str, service_names: list[str], time: datetime):
        pet = next((p for p in self._pets if p.name == pet_name), None)
        if not pet:
            print(f"No pet named {pet_name} found.")
            return

        # Check if clinic supports scheduling
        if not hasattr(clinic, "schedule_appointment"):
            print(f"Clinic '{clinic}' does not support appointment scheduling.")
            return

        # Schedule via clinic or via client
        # appointment = clinic.schedule_appointment(self, pet, service_names, time)
        # if not appointment:
        #     print("Appointment not scheduled by clinic.")
        #     return

        # Construct Appointment object from client side
        appointment = Appointment.from_client(
            pet=pet,
            business=clinic,
            services=[s for s in clinic._services if s.name in service_names],
            appointment_time=time,
            employee=None  # Let the clinic assign employee
        )

        self._appointments.append(appointment)
        if clinic not in self._vets:
            self._vets.append(clinic)
        print(f"Appointment scheduled at {clinic._name} for {pet.name} on {time}.")
    def add_medical_record(self, pet_name: str, record: str):
        for pet in self._pets:
            if pet.name == pet_name:
                pet.add_medical_record(record)
                print(f"Medical record added to {pet_name}: '{record}'")
                return
        print(f"No pet named {pet_name} found.")

    def add_toy(self, pet_name: str, toy: str):
        for pet in self._pets:
            if pet.name == pet_name:
                pet.add_toy(toy)
                print(f"Added toy '{toy}' to {pet_name}.")
                return
        print(f"No pet named {pet_name} found.")

    def play_with_pet(self, pet_name: str):
        for pet in self._pets:
            if pet.name == pet_name:
                pet.play_with(self)
                return
        print(f"No pet named {pet_name} found.")

    def feed_pet(self, pet_name: str):
        for pet in self._pets:
            if pet.name == pet_name:
                pet.feed()
                return
        print(f"No pet named {pet_name} found.")

    def rest_pet(self, pet_name: str):
        for pet in self._pets:
            if pet.name == pet_name:
                pet.rest()
                return
        print(f"No pet named {pet_name} found.")

    def show_all_statuses(self):
        for pet in self._pets:
            print(pet.status())
###########################TESTING##########################################

if __name__ == "__main__":
    print("--- Testing PetOwner ---")
    from models.animals import Feline
    # Create a PetOwner (not just a Human!)
    sara = PetOwner(
        name="Sara",
        dob=date(2001, 10, 17),
        sex="F",
        race="Caucasian",
        weight=54.0,
        height=165.0,
        phone="555-7890",
        email="alice@example.com")
    print(sara)

    mylo = Feline(name="Mylo", dob=date(2020, 7, 4), sex="M", weight=4.5, height=21.0,
                  diet=DietType.CARNIVORE, feline_type="Cat", breed="Domestic Shorthair")

    mochi = Feline(name="Mochi", dob=date(2020, 7, 4), sex="M", weight=9, height=25.0,
                  diet=DietType.CARNIVORE, feline_type="Cat", breed="Domestic Shorthair")

    pet_cat_mylo = sara.add_pet(animal=mylo, microchipped=True, neutered_or_sprayed = True)
    pet_cat_mochi = sara.add_pet(animal=mochi, microchipped=True, neutered_or_sprayed = False)

    # Test contact info and pet list
    print(sara.get_contact_info())
    print(sara.list_pets())

    # Pet interaction
    sara.play_with_pet("Mylo")
    sara.feed_pet("Mylo")
    sara.rest_pet("Mylo")

    # Toy and medical record
    sara.add_toy("Mylo", "Laser pointer")
    sara.add_medical_record("Mochi", "Neutered on 2022-06-10")

    # Show final status
    sara.show_all_statuses()