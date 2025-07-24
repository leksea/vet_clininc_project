from datetime import datetime
from typing import Optional, List
from services.service import Service
from services.employee import Employee
from services.businessservice import BusinessService
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.pet import Pet

class Appointment:
    def __init__(self,
                 client_id: str,
                 pet_id: str,
                 service_ids: List[str],
                 appointment_time: datetime,
                 employee_id: Optional[str] = None,
                 business_id: Optional[str] = None,
                 services: list[Service] = None):
        self._client_id = client_id
        self._pet_id = pet_id
        self._service_ids = service_ids
        self._time = appointment_time
        self._employee_id = employee_id
        self._business_id = business_id
        self._services = services if services else []
    @property
    def time(self): return self._time
    @property
    def employee_id(self): return self._employee_id
    @property
    def business_id(self): return self._business_id
    @property
    def pet(self): return self._pet_id
    @property
    def services(self): return self._services

    def total_cost(self) -> float:
        return sum(s.price for s in self._services)

    @classmethod
    def from_business(cls,
                      client_id: str,
                      pet_id: str,
                      service_ids: List[str],
                      appointment_time: datetime,
                      employee_id: Optional[str] = None,
                      business_id: Optional[str] = None):
        return cls(client_id, pet_id, service_ids, appointment_time, employee_id, business_id)

    @classmethod
    def from_client(cls,
                    pet: "Pet",
                    business: BusinessService,
                    services: List[Service],
                    appointment_time: datetime,
                    employee: Optional[Employee] = None):
        client_id = None
        pet_id = pet.name
        service_ids = [s.name for s in services]
        business_id = business._name
        employee_id = employee._name if employee else None

        return cls(client_id, pet_id, service_ids, appointment_time,
                   employee_id=employee_id, business_id=business_id, services=services)

    def __str__(self):
        return (f"Appointment[Client: {self._client_id}, Pet: {self._pet_id}, "
                f"Services: {self._service_ids}, Time: {self._time}, "
                f"Employee: {self._employee_id}, Business: {self._business_id}]")

###########################TESTING##########################################
if __name__ == "__main__":
    print("--- Testing Appointment ---")

    # -------- From Business Perspective --------
    client_id = "C12345"
    pet_id = "P78901"
    service_ids = ["Vaccination", "Checkup"]
    appointment_time = datetime(2025, 8, 15, 10, 0)
    employee_id = "E2222"
    business_id = "Dr Sawyer's Clininc"

    appt_business = Appointment.from_business(
        client_id=client_id,
        pet_id=pet_id,
        service_ids=service_ids,
        appointment_time=appointment_time,
        employee_id=employee_id,
        business_id=business_id
    )
    print("Business:")
    print(appt_business)

    # -------- From Client Perspective --------
    appointment_time = datetime(2025, 8, 16, 14, 30)
    services = [
        Service("Cat Neutering", "Surgery", 5, 100.0),
        Service("Cat Exam", "Wellness", 3, 50.0)
    ]

    class DummyPet:
        def __init__(self, name):
            self.name = name

    class DummyVetClinic:
        def __init__(self, name):
            self._name = name

    class DummyEmployee:
        def __init__(self, name):
            self._name = name

    pet = DummyPet("Mr Meow")
    clinic = DummyVetClinic("Dr Sawyer's Clininc")
    employee = DummyEmployee("Dr. Sawyer")

    appt_client = Appointment.from_client(
        pet=pet,
        business=clinic,
        services=services,
        appointment_time=appointment_time,
        employee=employee
    )
    print("Client:")
    print(appt_client)