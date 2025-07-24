from models.animals import Animal, DietType
from models.human import Human
from datetime import date
#----------------PET---------------------
class Pet:
    def __init__(self, animal: Animal, owner: Human, microchipped: bool = False, neutered_or_sprayed: bool = False):
        self._animal = animal
        self._owner = owner
        self._microchipped = microchipped
        self._neutered_or_sprayed = neutered_or_sprayed
        self._medical_records = []
        self._hunger = 0  # 0 = full, 10 = starving
        self._anxiety = 0  # 0 = calm, 10 = max stress
        self._traits = {"shy": False, "playful": True, "curious": True}
        self._toys = []

    @property
    def name(self): return self._animal.name
    @property
    def owner(self): return self._owner.name
    @property
    def type(self): return self._animal._type
    @property
    def age(self): return self._animal.age
    @property
    def weight(self): return self._animal._weight
    @property
    def sex(self): return self._animal._sex
    @property
    def breed(self): return self._animal._breed

    def add_medical_record(self, record: str):
        self._medical_records.append(record)

    def add_toy(self, toy: str):
        self._toys.append(toy)

    def play_with(self, human: Human):
        if human.name == self._owner.name or not self._traits["shy"]:
            print(f"{self._animal.name} is playing with {human.name}.")
            self._hunger = min(10, self._hunger + 1)
            self._anxiety = max(0, self._anxiety - 1)
        else:
            print(f"{self._animal.name} is too shy to play with {human.name}.")

    def feed(self):
        print(f"Feeding {self._animal.name}...")
        self._hunger = 0

    def visit_vet(self):
        print(f"{self._animal.name} is visiting the vet.")
        self._medical_records.append("Vet visit")
        self._anxiety = max(10, self._anxiety + 5)

    def rest(self):
        print(f"{self._animal.name} is resting.")
        self._anxiety = max(0, self._anxiety - 1)

    def status(self):
        return f"{self._animal.name}: Hunger={self._hunger}/10, Anxiety={self._anxiety}/10"

    def __str__(self):
        return (f"Pet {self.name} "
                f"({self.type}) "
                f"owned by {self._owner.name}"
                f" breed: {self.breed} "
                f" weight: {self.weight}"
                f" age: {self.age}"
                f" sex: {self.sex}"                
                f" Neutered or sprayed: {self._neutered_or_sprayed}")
###########################TESTING##########################################
if __name__ == "__main__":
    print("--- Testing Pet ---")
    from models.animals import Feline
    # Create a human owner
    sara = Human(name="Sara", dob=date(2001, 10, 17), sex="F", race="Caucasian", weight=54.0, height=165.0)

    # Create a pet animal - Feline
    mylo = Feline(name="Mylo", dob=date(2020, 7, 4), sex="M", weight=4.5, height=25.0,
                   diet=DietType.CARNIVORE, feline_type="Cat", breed="Domestic Shorthair")

    # Wrap in a Pet object
    pet_cat = Pet(animal=mylo, owner=sara, microchipped=True, neutered_or_sprayed=True)

    # Interactions
    print(pet_cat)  # __str__
    print(pet_cat.status())  # Initial status

    pet_cat.play_with(sara)  # Should play with owner
    print(pet_cat.status())  # Hunger should increase, anxiety decrease

    stranger = Human(name="Bob", dob=date(1985, 3, 2), sex="M", race="Asian", weight=70, height=175)
    pet_cat.play_with(stranger)  # May or may not play depending on 'shy' trait

    pet_cat.feed()  # Reset hunger
    print(pet_cat.status())

    pet_cat.visit_vet()  # Anxiety arises
    pet_cat.add_medical_record(f"Vet visit {date.today()}")
    print(pet_cat.status())
    print(pet_cat._medical_records)

    pet_cat.rest()  # Additional rest
    print(pet_cat.status())

    pet_cat.add_toy("Laser pointer")  # Add toy
    pet_cat.add_medical_record("Neutered on 2022-06-10")
    print(pet_cat)
