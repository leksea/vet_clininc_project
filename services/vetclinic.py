from services.businessservice import BusinessService
from services.appointment import Appointment
from services.employee import Employee
from services.service import Service
from models.client import Client
from models.pet import Pet
from models.petowner import PetOwner
from models.animals import *
from datetime import datetime, date, timedelta
from typing import Optional, List
import random as rd
import os
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


class VetClinic(BusinessService):
    def __init__(self, name: str, location: str, phone: str, hours: str, ownership: str, specialty: str,
                 services: Optional[List[Service]] = None,
                 employees: Optional[List[Employee]] = None,
                 clients: Optional[List[Client]] = None,
                 is_hiring: bool = False,
                 is_open: bool = False,
                 accepts_new_clients: bool = True):
        super().__init__(name, location, phone, hours, ownership, specialty,
                         services, employees, clients or [], is_hiring, is_open)
        self._appointments: List[Appointment] = []
        self._accepts_new_clients = accepts_new_clients
        self._todays_staff = {}
        self._role_services = {
            "Receptionist": [],
            "VetTech": {"Vaccination", "Checkup"},
            "Vet": {"Vaccination", "Checkup", "Neutering", "Surgery"}
        }
    @property
    def receptionist(self): return self._todays_staff.get("Receptionist")
    @property
    def vettech(self): return self._todays_staff.get("VetTech")
    @property
    def vet(self): return self._todays_staff.get("Vet")

    def validate_role(self, employee, allowed_roles: list[str]) -> bool: # checks that role matches Services
        if employee.role not in allowed_roles:
            print(f"Access denied: '{employee.name}' is a '{employee.role}', not allowed to perform this action.")
            return False
        return True

    def get_employees_by_role(self, role: str) -> List[Employee]: # todo store employyes by roles
        return [e for e in self._employees if e.role == role]

    def add_employee(self, employee: Employee):  # add employee
        if employee.role not in self._role_services:
            raise ValueError(f"Unknown role: {employee.role}")
        self._employees.append(employee)
        print(f"Employee '{employee.name}' added as '{employee.role}'.")

    def remove_employee(self, employee: Employee): #remove employee
        if employee in self._employees:
            self._employees.remove(employee)
            print(f"Employee '{employee.name}' removed.")

    def open_business(self): # opens clininc and assigns receptionist, vet tech and vet
        self._is_open = True
        print(f"{self._name} is now open.")

        # Randomlyu assign one receptionist, one vet tech, and one vet for the day
        roles_to_assign = ["Receptionist", "VetTech", "Vet"]
        self._todays_staff = {}

        for role in roles_to_assign:
            eligible = self.get_employees_by_role(role)
            if eligible:
                selected = rd.choice(eligible)
                self._todays_staff[role] = selected
                print(f"{role} on duty today: {selected.name}")
            else:
                print(f"No available {role} for today.")

    def close_business(self):
        self._is_open = False
        self._todays_staff = {} # release the staff
        print(f"{self._name} is now closed.")

    def create_client(self, pet_owner: PetOwner, pet: Pet, requester: Employee = None) -> Client: # create client in a separate to match BusinessService
        if requester is None: # Only receptionist can create clients
            requester = self.receptionist
        if not self.validate_role(requester, ["Receptionist"]):
            return None
        new_client = Client(pet_owner, pet, primary_vet_id=self._name)
        self._clients.append(new_client)
        print(f"Client '{new_client.firstname}' (Owner: {new_client.lastname}) added by {requester.id}.")
        return new_client

    def add_client(self, new_client:Client) -> None: # Match BusinessService method
        if not self._accepts_new_clients:
            print("Clinic is not accepting new clients.")
            return None
        self._clients.append(new_client)

        # Save new client to file
        with open(os.path.join(DATA_DIR, "Clients.txt"), "a") as f:
            f.write(f"{new_client.client_id},"
                    f"{new_client.firstname},"
                    f"{new_client.lastname},"
                    f"{new_client.phone_number},"
                    f"{new_client.dob},"
                    f"{new_client.type},"
                    f"{new_client.breed},"
                    f"{new_client.primary_vet_id}\n")

        print(f"Client '{new_client.firstname}' (Owner: {new_client.owner_name}) added.")
        return new_client

    def lookup_client_by_pet(self, pet_name: str, last_name: str, phone: str) -> List[Client]: # not in use
        matches = []
        for client in self._clients:
            if (client.firstname.lower() == pet_name.lower() and
                client.lastname.lower() == last_name.lower() and
                client.phone_number == phone):
                matches.append(client)
        return matches

    def remove_client(self, client: Client):
        if client in self._clients:
            self._clients.remove(client)
            print(f"Client '{client.firstname}' removed.")

    def is_available(self, requested_time: datetime) -> bool: #check if appointment time is available
        return all(appt.time != requested_time for appt in self._appointments)

    def schedule_appointment(self, client: Client, services: list[Service], employees: list["Employee"] = None):
        """
        :param client:
        :param services:
        :param employees:
        :return: appointment
        Clumsy implementation:
        # Offer 3 random appointment time slots
        get input from user
        assign first available employee
        add employee to client's calendar and
        """
        print(f"Available time slots for {client.pet.name}:")
        options = []
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        for _ in range(3):
            random_hour = rd.randint(9, 16)
            random_day = rd.randint(1, 10)
            slot = now.replace(hour=random_hour) + timedelta(days=random_day)
            options.append(slot)

        for i, slot in enumerate(options, 1):
            print(f"{i}. {slot.strftime('%Y-%m-%d %H:%M')}")

        try:
            choice = int(input("Select a time (1-3): "))
            if choice not in (1, 2, 3):
                print("Invalid choice.")
                return False
        except ValueError:
            print("Invalid input.")
            return False

        selected_time = options[choice - 1]

        if not self.is_available(selected_time):
            print("That time slot is already taken.")
            return False

        # Assign first available employee if not given -- needs improvement
        selected_employee = employees[0] if employees else None

        appointment = Appointment.from_client(
            pet=client.pet,
            business=self,
            services=services,
            appointment_time=selected_time,
            employee=selected_employee
        )
        if selected_employee:
            appointment._employee_id = selected_employee.id

        self._appointments.append(appointment)
        client.add_appointment(appointment) # propagate to pet owner

        # Save to Appointments file
        with open(os.path.join(DATA_DIR, "Appointments.txt"), "a") as f:
            f.write(f"{client.client_id},{client.pet.name},{','.join(s.name for s in services)},{selected_time}\n")
        print(f"Appointment for {client.pet.name} scheduled on {selected_time}.")
        return appointment

    # Start Appointment
    def start_appointment(self, client: Client, appointment: Appointment, employees: list["Employee"] = None):
        """

        :param client:
        :param appointment:
        :param employees:
        :return: None

        clumsy implementation
        If we can't find assigned employee in list of employess, assign today's vet tech
        Do services, remove them from appointment, display erroe messages if not enough skills to do service
        Log Services
        Provide total
        Remove appointment
        """
        if self._employees is None:
            print("Can't start appointment for this client, no employees available.")
        if appointment not in self._appointments:
            print(f"Appointment for {client.pet.name} not found in system.")
            return

        assigned_employee = next((e for e in self._employees if e.id == appointment.employee_id), None)
        # if assigned employee exists, is must be in the list
        if assigned_employee and (employees is None or assigned_employee not in employees):
            employees = (employees or []) + [assigned_employee]

        if not assigned_employee:
            assigned_employee = self.vettech
        # sdd service records to pet's medical history
        for service in appointment.services:
            if not any(service.name in self._role_services.get(e.role, set()) for e in (employees or [])):
                print(f"Warning: No assigned employee is authorized to perform '{service.name}'. Skipping.")
                appointment.services.remove(service)
                continue
            else:
                record = f"{appointment.time}: Received {service.name} by Employee {assigned_employee.id}"
                client.pet.add_medical_record(record)

        total = appointment.total_cost()

        with open(os.path.join(DATA_DIR, "Appointments.txt"), "a") as f:

            f.write(
                f"{client.client_id},"
                f"{client.pet.name},"
                f"{appointment.time},"
                f"{assigned_employee.id},"                
                f"{', '.join(s.name for s in appointment.services)},"
                f"${total:.2f}\n"
            )

        # Remove appointment
        self._appointments.remove(appointment)
        client.remove_appointment(appointment)
        # Print out services
        if employees:
            emp_names = ", ".join(e.name for e in employees)
            print(f"Services performed by: {emp_names}")

        print(f"Appointment for {client.pet.name} complete. Total cost: ${total:.2f}")
###########################TESTING##########################################
if __name__ == "__main__":
    print("--- Testing Vet Clininc ---")

    # Create dummy services
    vaccination = Service(name="Vaccination", specialty="Wellness", experience=2, price=45.0)
    checkup = Service(name="Checkup", specialty="Wellness", experience=2, price=30.0)

    # Create a vet clinic
    clinic = VetClinic(
        name="Happy Paws Vet",
        location="123 Main St",
        phone="555-9876",
        hours="9am-5pm",
        ownership="Private",
        specialty="Cats & Dogs",
        services=[vaccination, checkup]
    )
    # Create and hire a VetTech employee who can perform Vaccination and Checkup
    vettech = Employee(
        name="Alex VetTech",
        dob=date(1990, 5, 20),
        sex="M",
        race="White",
        weight=70,
        height=175,
        diet=DietType.OMNIVORE,
        role="VetTech"
    )
    # Create and hire a Receptionist employee who can register client

    receptionist = Employee(
        name="Maria Reception",
        dob=date(1999, 1, 5),
        sex="F",
        race="White/Hispanic",
        weight=70,
        height=175,
        diet=DietType.OMNIVORE,
        role="Receptionist"
    )

    clinic.add_employee(vettech)
    clinic.add_employee(receptionist)

    # Create a pet owner and pet
    jane_owner = PetOwner(
        name="Jane Doe",
        dob=date(1985, 6, 15),
        sex="F",
        race="White",
        weight=60,
        height=165,
        phone="555-1234",
        email="jane@example.com"
    )

    # Create a Feline animal and wrap it in a Pet
    kitty = Feline(
        name="Mittens",
        dob=date(2020, 3, 14),
        sex="F",
        weight=4.5,
        height=25.0,
        diet=DietType.CARNIVORE,
        feline_type="Cat",
        breed="Ragdoll"
    )
    kitty_pet = Pet(animal=kitty, owner=jane_owner)

    # Add client
    client_happy_paws = clinic.create_client(pet_owner=jane_owner, pet=kitty_pet, requester = receptionist)
    clinic.add_client(client_happy_paws)

    # Schedule an appointment
    appt_time = datetime(2025, 8, 10, 14, 0)
    kitty_appointment = clinic.schedule_appointment(
        client=client_happy_paws,
        services=[vaccination, checkup],
        employees=[vettech]
    )
    # Start the appointment using the returned appointment
    if kitty_appointment:
        clinic.start_appointment(
            client=client_happy_paws,
            appointment=kitty_appointment)