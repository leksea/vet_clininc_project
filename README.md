# vet_clininc_project
Vet Clinic Project for CIST-005A-54250


# 🐈 🐕 🐎  This is a virtual Vet Clinic Simulation 🐇 🦎 🐍 

A Python-based object-oriented simulation of a veterinary clinic. It models real-world operations such as scheduling appointments, managing clients and pets, and assigning staff to perform services. Designed with modularity and extensibility in mind.
Basic version, multiple improvements incoming. 

## Project Structure
<pre lang="markdown">
.
├── main.py                   # Entry point script to simulate clinic operations
├── data/                     # Output folder for saved appointments and clients
├── models/
│   ├── animals.py            # Base Animal class and specific types (Canine, Feline, etc.)
│   ├── client.py             # Client class linking pet and pet owner
│   ├── pet.py                # Pet wrapper for an animal with medical records
│   ├── petowner.py           # Pet owner class with contact info
│   ├── human.py              # Base Human class (common attributes)
├── services/
│   ├── appointment.py        # Appointment class with time, services, and assigned employee
│   ├── businessservice.py    # Base class for the clinic (BusinessService)
│   ├── employee.py           # Employee class (Vet, VetTech, Receptionist)
│   ├── service.py            # Service class with type, price, and duration
│   └── vetclinic.py          # Core clinic logic and business rules
</pre>

## Diagram
<img src="images/VetClininc.png" alt="UML Diagram" width="600"/>

## Features

- Object-oriented class design with inheritance and encapsulation
- Employees assigned roles (`Vet`, `VetTech`, `Receptionist`) and duties
- Clients and pets modeled with proper associations
- Support for medical services (e.g., checkup, vaccination, neutering)
- Role-based permissions for scheduling, handling clients, and executing services
- Randomized daily staffing with appointment validation
- Outputs appointment and client records to `.txt` files

## How to Run

1. Clone this repo or download the source code.
2. Navigate to the project directory.
3. Ensure dependencies (if any) are installed (Python 3.10+ recommended).
4. Run the main simulation:

```bash
python main.py
