from models.human import Human
from services.service import Service
from datetime import date
import string
import random as rd
from models.animals import DietType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.client import Client

class Employee(Human):
    def __init__(self, name: str, dob: date, sex: str, race: str,
                 weight: float, height: float, diet: DietType,
                 role: str, is_vaccinated: bool = True):
        super().__init__(name, dob, sex, race, weight, height, diet)
        self._role = role
        self._is_vaccinated = is_vaccinated
        self._employee_id = ''.join(rd.choices(string.ascii_letters + string.digits, k=6))
        self._services_offered = []
    @property
    def role(self) -> str: return self._role
    @property
    def id(self) -> str: return self._employee_id


    def get_info(self):
        return f"{self.name} ({self._role}) - ID: {self._employee_id}"

    def perform_service(self, client: "Client", service: Service):
        print(f"{self.id} is performing {service.name} on {client.firstname, client.lastname}.")
        client.add_medical_record(f"{date.today()}: {service.name} performed by {self.id}")

    def remove_service(self, service: Service):
        if service in self._services_offered:
            self._services_offered.remove(service)
            print(f"Service '{service.name}' removed.")

    def add_service(self, service: Service):
        if service not in self._services_offered:
            self._services_offered.append(service)
            print(f"Service '{service.name}' added.")

if __name__ == "__main__":
    print("--- Testing Employee ---")
    from services.service import Service
    from models.animals import DietType
    from datetime import date

    class TestClient:
        def __init__(self, name):
            self.firstname = name
            self.lastname = name
            self.records = []

        def add_medical_record(self, record: str):
            print(f"[Client Record] {record}")
            self.records.append(record)

    # Create an employee
    vet = Employee(
        name="Dr. Ken Sawyer",
        dob=date(1945, 3, 10),
        sex="M",
        race="Caucasian",
        weight=68.0,
        height=170.0,
        diet=DietType.OMNIVORE,
        role="Veterinarian"
    )

    # Create a service
    neutering = Service(name="Neutering", specialty="Surgery", experience=5, price=520.0)

    # Add service to vet
    vet.add_service(neutering)

    # Create a mock client
    bruno = TestClient("Bruno")

    # Perform service
    vet.perform_service(bruno, neutering)

    # Print employee info
    print(vet.get_info())