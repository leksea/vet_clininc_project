from abc import ABC, abstractmethod
from typing import List
from services.service import Service
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.appointment import Appointment
    from services.employee import Employee
    from models.client import Client

#-------------BusinessService---------------
class BusinessService(ABC):
    def __init__(self,
                 name: str,
                 location: str,
                 phone: str,
                 hours: str,
                 ownership: str,
                 specialty: str,
                 services: List[Service] = None,
                 employees: List["Employee"] = None,
                 clients: List["Client"] = None,
                 is_hiring: bool = False,
                 is_open: bool = False):
        self._name = name
        self._location = location
        self._phone = phone
        self._hours = hours
        self._ownership = ownership
        self._specialty = specialty
        self._employees = employees if employees else []
        self._clients = clients if clients else []
        self._services = services if services else []
        self._is_hiring = is_hiring
        self._is_open = is_open

    @abstractmethod
    def open_business(self): pass

    @abstractmethod
    def close_business(self): pass

    @abstractmethod
    def add_client(self, client): pass

    @abstractmethod
    def remove_client(self, client): pass

    @abstractmethod
    def add_employee(self, employee): pass

    @abstractmethod
    def remove_employee(self, employee): pass

    @abstractmethod
    def schedule_appointment(self, client:"Client", services:list[Service], employees:list["Employee"] = None): pass

    @abstractmethod
    def start_appointment(self, client:"Client", appointment:"Appointment", employees:list["Employee"] = None): pass

    def add_service(self, service: Service):
        self._services.append(service)
        print(f"Service '{service.name}' added.")

    def remove_service(self, service: Service):
        if service in self._services:
            self._services.remove(service)
            print(f"Service '{service.name}' removed.")

    def get_services(self) -> List[str]:
        return [service.name for service in self._services]
