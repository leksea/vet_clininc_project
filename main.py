from services.vetclinic import VetClinic
from datetime import date
from services.employee import Employee
from services.service import Service
from models.petowner import PetOwner
from models.pet import Pet
from models.animals import Feline, DietType
from services.vetclinic import VetClinic



# Create empty clinic
clinic = VetClinic(name="Dr Sawyer's Practicee ", location="101 Murphy Ave, Sunnyvale, CA, 94089 ", phone="555-8888",
                   hours="8am-3pm", ownership="Private", specialty="General")

# Hire staff
receptionist1 = Employee(
    name="Maria Reception1",
    dob=date(1999, 1, 5),
    sex="F",
    race="White/Hispanic",
    weight=70,
    height=175,
    diet=DietType.OMNIVORE,
    role="Receptionist"
)
receptionist2 = Employee(
    name="Carly Reception2",
    dob=date(2004, 2, 23),
    sex="N/A",
    race="Asian",
    weight=60,
    height=165,
    diet=DietType.HERBIVORE,
    role="Receptionist"
)

vettech1 = Employee(
    name="Alex VetTech1",
    dob=date(1990, 5, 20),
    sex="M",
    race="White",
    weight=70,
    height=175,
    diet=DietType.OMNIVORE,
    role="VetTech"
)
vettech2 = Employee(
    name="Diane VetTech2",
    dob=date(1987, 3, 3),
    sex="F",
    race="White",
    weight=76,
    height=160,
    diet=DietType.OMNIVORE,
    role="VetTech"
)
vet = Employee(
    name="Dr Ken Sawyer",
    dob=date(1956, 6, 11),
    sex="M",
    race="White",
    weight=76,
    height=180,
    diet=DietType.OMNIVORE,
    role="Vet"
)

for emp in [receptionist1, receptionist2, vettech1, vettech2, vet]:
    clinic.add_employee(emp)

clinic.open_business()
#+++++++++++++++++++++++++++++++++++++++++++++
# Receptionist adds a client

owner = PetOwner(name="Jane Doe", dob=date(1990, 1, 1), sex="F", race="White",
                 weight=58, height=165, phone="555-7890", email="jane.doe@gmail.com")
cat1 = Feline(name="Xander", dob=date(2020, 5, 5), sex="M", weight=10.0, height=50.0,
               diet=DietType.CARNIVORE, feline_type="Cat", breed="Maine Coon")

cat2 = Feline(name="Danielle", dob=date(2021, 7, 15), sex="F", weight=5.0, height=25.0,
               diet=DietType.CARNIVORE, feline_type="Cat", breed="Maine Coon")

pet1 = Pet(animal=cat1, owner=owner, microchipped=True, neutered_or_sprayed=False)
pet2 = Pet(animal=cat2, owner=owner, microchipped=True, neutered_or_sprayed=True)

owner.add_pet(pet1)
owner.add_pet(pet2)
print(pet1)
print(pet2)

client = clinic.create_client(owner, pet1)
clinic.add_client(client)

 # Schedule services (done manually )

vaccination = Service("Vaccination", "Wellness", 1, 40.0)
checkup = Service("Checkup", "Wellness", 3, 95.0)
neutering = Service("Neutering", "Surgery", 5, 550.0)

clinic.add_service(vaccination)
clinic.add_service(checkup)
clinic.add_service(neutering)

#
# Schedule simple chechup appointment
appt_simple = clinic.schedule_appointment(client, services=[vaccination, checkup], employees=[vettech1])
if appt_simple:
     clinic.start_appointment(client, appointment=appt_simple, employees=[vettech1])
#
# Try scheduling neutering with vet tech only
appt_complex_fail = clinic.schedule_appointment(client, services=[neutering], employees=[vettech2])
if appt_complex_fail:
    clinic.start_appointment(client, appointment=appt_complex_fail, employees=[vettech2])  # Should warn

# Schedule neutering with a vet
appt_complex_OK = clinic.schedule_appointment(client, services=[neutering], employees=[vet])
if appt_complex_OK:
    clinic.start_appointment(client, appointment=appt_complex_OK, employees=[vet])