from models.animals import Mammal, DietType
from datetime import date
# ----------------- Human Logic -----------------
class Human(Mammal):
    def __init__(self, name, dob, sex, race, weight, height, diet=DietType.OMNIVORE):
        super().__init__("Human", name, dob, sex, weight, height, diet, "Chordata", "Vertebrates", True, True, "Hominidae")
        self._race = race

    def makeSound(self): return "Hello"
    def getSpecies(self): return "Homo sapiens"
    def getFood(self): return "Balanced human diet"
    def hasFur(self): return False
    def walksOnHowManyLegs(self): return 2

    def __str__(self):
        return super().__str__() + f"| Race {self._race}  | Height: {self._height}"
###########################TESTING##########################################

if __name__ == "__main__":
    print("--- Testing Human ---")
    # Create human clients
    bob = Human(name="Bob", dob=date(1985, 3, 2), sex="M", race="Asian", weight=70, height=175)
    carol = Human(name="Carol", dob=date(1992, 9, 10), sex="F", race="White/Hispanic", weight=55, height=160)
    print(bob)
    print(carol)