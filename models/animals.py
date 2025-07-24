from datetime import date
from enum import Enum
from abc import ABC, abstractmethod

# ----------------- DietType Enum -----------------
class DietType(Enum):
    CARNIVORE = "Carnivore"
    HERBIVORE = "Herbivore"
    OMNIVORE = "Omnivore"

# ----------------- Animal Base Class -----------------
class Animal(ABC):
    def __init__(self, animal_type: str, name: str, dob: date, sex: str, weight: float, height: float = None,
                 diet: DietType = None, is_domesticated: bool = False, is_vaccinated: bool = False,
                 kingdom: str = "Animalia", phylum: str = "", animal_class: str = "", group: str = ""):
        self._type = animal_type
        self._name = name
        self._dob = dob
        self._sex = sex
        self._weight = weight
        self._height = height
        self._diet = diet
        self._is_domesticated = is_domesticated
        self._vaccinated = is_vaccinated
        self._kingdom = kingdom
        self._phylum = phylum
        self._animal_class = animal_class
        self._group = group

    @property
    def name(self): return self._name

    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))

    @abstractmethod
    def makeSound(self): pass

    @abstractmethod
    def getSpecies(self): pass

    @abstractmethod
    def getFood(self): pass

    def __str__(self):
        return f"{self._type} | Name: {self._name} | Age: {self.age} | Sex: {self._sex} | Weight: {self._weight}"

# ----------------- Mammal Abstract Class -----------------
class Mammal(Animal):
    def __init__(self, animal_type: str, name: str, dob: date, sex: str, weight: float, height: float, diet: DietType,
                 phylum: str, group: str, is_domesticated: bool, is_vaccinated: bool = False, subtype: str = None):
        super().__init__(animal_type, name, dob, sex, weight, height, diet, is_domesticated, is_vaccinated,
                         animal_class="Mammalia", phylum=phylum, group=group)
        self._subtype = subtype

    @abstractmethod
    def hasFur(self): pass

    @abstractmethod
    def walksOnHowManyLegs(self): pass

# ----------------- Specific Animal Classes -----------------
class Canine(Mammal):
    def __init__(self, name, dob, sex, weight, height, diet, canine_type, breed, is_domesticated=True, is_vaccinated=False):
        super().__init__("Canine", name, dob, sex, weight, height, diet, "Chordata", "Vertebrates", is_domesticated, is_vaccinated, "Canine")
        self._breed = breed
        self._type = canine_type

    def makeSound(self): return "Bark"
    def getSpecies(self): return "Canis lupus familiaris"
    def getFood(self): return "Meat"
    def hasFur(self): return True
    def walksOnHowManyLegs(self): return 4

class Feline(Mammal):
    def __init__(self, name, dob, sex, weight, height, diet, feline_type, breed, is_domesticated=True, is_vaccinated=False):
        super().__init__("Feline", name, dob, sex, weight, height, diet, "Chordata", "Vertebrates", is_domesticated, is_vaccinated, "Feline")
        self._breed = breed
        self._type = feline_type

    def makeSound(self): return "Meow"
    def getSpecies(self): return "Felis catus"
    def getFood(self): return "Meat"
    def hasFur(self): return True
    def walksOnHowManyLegs(self): return 4

class Rodent(Mammal):
    def __init__(self, name, dob, sex, weight, height, diet, rodent_type, breed, is_domesticated=True, is_vaccinated=False):
        super().__init__("Rodent", name, dob, sex, weight, height, diet, "Chordata", "Vertebrates", is_domesticated, is_vaccinated, "Rodent")
        self._breed = breed
        self._type = rodent_type

    def makeSound(self): return "Squeak"
    def getSpecies(self): return "Rodentia"
    def getFood(self): return "Pellets, seeds, or vegetables"
    def hasFur(self): return True
    def walksOnHowManyLegs(self): return 4


class Fish(Animal):
    def __init__(self, name, dob, sex, weight, length, diet, fish_type, breed,  height=None, is_domesticated=True, is_vaccinated=False):
        super().__init__("Fish", name, dob, sex, weight, height, diet, phylum="Chordata", group="Vertebrates",
                         is_domesticated=is_domesticated, is_vaccinated=is_vaccinated)
        self._breed = breed
        self._type = fish_type
        self._length = length


    def makeSound(self): return "Blub"
    def getSpecies(self): return "Actinopterygii"
    def getFood(self): return "Fish flakes"

class Reptile(Animal):
    def __init__(self, name, dob, sex, weight, length, diet, reptile_type, breed, height = None, is_domesticated=False, is_vaccinated=False, is_venomous=False):
        super().__init__("Reptile", name, dob, sex, weight, height, diet, phylum="Chordata", group="Reptilia",
                         is_domesticated=is_domesticated, is_vaccinated = is_vaccinated)
        self._breed = breed
        self._type = reptile_type
        self._length = length
        self._is_venomous = is_venomous


    def makeSound(self): return "Hiss"
    def getSpecies(self): return "Generic Reptile"
    def getFood(self): return "Insects or small rodents"


###########################TESTING##########################################
if __name__ == '__main__':

    print("--- Testing Animals ---")
    # Create animals
    snake = Reptile(name="Miss Hisses", dob=date(2018, 6, 1), sex="M", weight=2.3, length=120, diet=DietType.CARNIVORE,
                    reptile_type="Snake", breed="Ball Python", is_venomous=False)

    rabbit = Rodent(name="Hopper", dob=date(2021, 3, 15), sex="F", weight=1.5, height=20.0, diet=DietType.HERBIVORE,
                    rodent_type="Rabbit", breed="Holland Lop")

    dog = Canine(name="Buddy", dob=date(2019, 12, 25), sex="M", weight=20.0, height=50.0, diet=DietType.OMNIVORE,
                 canine_type="Dog", breed="Labrador")

    chinchilla = Rodent(name="Dusty", dob=date(2022, 1, 1), sex="M", weight=0.8, height=15.0, diet=DietType.HERBIVORE,
                        rodent_type="Chinchilla", breed="Standard Gray")

    lizard = Reptile(name="Spike", dob=date(2020, 8, 8), sex="F", weight=0.6, length=25, diet=DietType.OMNIVORE,
                     reptile_type="Lizard", breed="Bearded Dragon", is_venomous=False)


    # Run basic interactions
    for creature in [snake, rabbit, dog, chinchilla, lizard]:
        print("-----------------------------")
        print(creature)
        print(creature.makeSound())
        print(creature.getSpecies())
        print(creature.getFood())
