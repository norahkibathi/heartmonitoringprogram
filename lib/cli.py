import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Doctor, Patient, FitnessExpert

DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# the function enables the user to interact with display menu function
def display_menu():
    print("Welcome to the Heart Health Management System")
    print("1. Manage Doctors")
    print("2. Manage Patients")
    print("3. Manage Fitness Experts")
    print("4. Exit")

# the function  registers a doctor
def register_doctor():
    print("Register a Doctor")
    firstname = input("Enter doctor's first name: ")
    lastname = input("Enter doctor's last name: ")
    age = int(input("Enter doctor's age: "))
    gender = input("Enter doctor's gender: ")
    address = input("Enter doctor's address: ")
    email = input("Enter doctor's email: ")
    phone_number = input("Enter doctor's phone number: ")
    salary = float(input("Enter doctor's salary: "))
    working_hours = int(input("Enter doctor's working hours: "))
    # create a new instance of Doctor
    doctor = Doctor(firstname=firstname, lastname=lastname, age=age, gender=gender,
                    address=address, email=email, phone_number=phone_number,
                    salary=salary, working_hours=working_hours)
    # the code block adds the new doctor to the session and commit the transaction
    session.add(doctor)
    session.commit()
    print("Doctor registered successfully!")

# the function enables  to view doctor details
def view_doctor_details():
    doctor_id = int(input("Enter doctor's ID: "))
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        print("Doctor Details:")
        print(f"Name: {doctor.firstname} {doctor.lastname}")
        print(f"Age: {doctor.age}")
        print(f"Gender: {doctor.gender}")
        print(f"Email: {doctor.email}")
        print(f"Address: {doctor.address}")
        print(f"Phone Number: {doctor.phone_number}")
        print(f"Working Hours: {doctor.working_hours}")
        print(f"Salary: {doctor.salary}")
        #the code block enables to  display patients assigned to this doctor
        if doctor.patients:
            print("Patients:")
            for patient in doctor.patients:
                print(f"- {patient.firstname} {patient.lastname}")
        else:
            print("No patients assigned to this doctor.")
    else:
        print("Doctor not found.")

# the function enables  to register a patient
def register_patient():
    print("Register a Patient")
    firstname = input("Enter patient's first name: ")
    lastname = input("Enter patient's last name: ")
    age = int(input("Enter patient's age: "))
    gender = input("Enter patient's gender: ")
    address = input("Enter patient's address: ")
    email = input("Enter patient's email: ")
    phone = input("Enter patient's phone number: ")
    diabetes = input("Does the patient have diabetes? (True/False): ").lower() == 'true'
    hypertension = input("Does the patient have hypertension? (True/False): ").lower() == 'true'
    smoking = input("Is the patient a smoker? (True/False): ").lower() == 'true'
    family_history = input("Does the patient have a family history of heart disease? (True/False): ").lower() == 'true'
    heart_failure = input("Has the patient experienced heart failure before? (True/False): ").lower() == 'true'
    
    weight = float(input("Enter patient's weight in kg (optional, press Enter to skip): ")) 
    height = float(input("Enter patient's height in cm (optional, press Enter to skip): "))
    
    # the functions enables  creation of  a new instance of Patient
    patient = Patient(firstname=firstname, lastname=lastname, age=age, gender=gender,
                      address=address, email=email, phone=phone,
                      diabetes=diabetes, hypertension=hypertension, smoking=smoking,
                      family_history=family_history, heart_failure=heart_failure,
                      weight=weight, height=height)

    # the code block enables calculation of risk score and category
    patient.calculate_risk_score()
    patient.get_risk_category()

    #the code block adds new patient to the session and commits the transaction
    session.add(patient)
    session.commit()

    print("Patient registered successfully!")

# the function enables to view patient details
def view_patient_details():
    patient_id = int(input("Enter patient's ID: "))
    patient = session.query(Patient).filter(Patient.id == patient_id).first()

    if patient:
        print("Patient Details:")
        print(f"Name: {patient.firstname} {patient.lastname}")
        print(f"Age: {patient.age}")
        print(f"Gender: {patient.gender}")
        print(f"Email: {patient.email}")
        print(f"Address: {patient.address}")
        print(f"Phone Number: {patient.phone}")
        print(f"Diabetes: {patient.diabetes}")
        print(f"Hypertension: {patient.hypertension}")
        # the functions enables to display risk score and category
        print(f"Risk Score: {patient.risk_score}")
        print(f"Risk Category: {patient.risk_category}")
        # the function enables to display doctor assigned to this patient
        if patient.doctor:
            print("Assigned Doctor:")
            print(f"- {patient.doctor.firstname} {patient.doctor.lastname}")
        else:
            print("No doctor assigned to this patient.")
    else:
        print("Patient not found.")

# the function enables  to register a fitness expert
def register_fitness_expert():
    print("Register a Fitness Expert")
    firstname = input("Enter fitness expert's first name: ")
    lastname = input("Enter fitness expert's last name: ")
    age = int(input("Enter fitness expert's age: "))
    gender = input("Enter fitness expert's gender: ")
    address = input("Enter fitness expert's address: ")
    email = input("Enter fitness expert's email: ")
    phone_number = input("Enter fitness expert's phone number: ")
    working_hours = int(input("Enter fitness expert's working hours: "))

    #the function  creates a new instance of FitnessExpert
    fitness_expert = FitnessExpert(firstname=firstname, lastname=lastname, age=age, gender=gender,
                                    address=address, email=email, phone_number=phone_number,
                                    working_hours=working_hours)

    #the code block  adds the new fitness expert to the session and commit the transaction
    session.add(fitness_expert)
    session.commit()
    
    print("Fitness expert registered successfully!")

# the function enables to view fitness expert details
def view_fitness_expert_details():
    fitness_expert_id = int(input("Enter fitness expert's ID: "))
    fitness_expert = session.query(FitnessExpert).filter(FitnessExpert.fitness_expert_id == fitness_expert_id).first()

    if fitness_expert:
        print("Fitness Expert Details:")
        print(f"Name: {fitness_expert.firstname} {fitness_expert.lastname}")
        print(f"Age: {fitness_expert.age}")
        print(f"Gender: {fitness_expert.gender}")
        print(f"Email: {fitness_expert.email}")
        print(f"Address: {fitness_expert.address}")
        print(f"Phone Number: {fitness_expert.phone_number}")
        print(f"Working Hours: {fitness_expert.working_hours}")
        print(f"Salary: {fitness_expert.salary}")
        # the function displays patients assigned to this fitness expert
        if fitness_expert.patients:
            print("Patients:")
            for patient in fitness_expert.patients:
                print(f"- {patient.firstname} {patient.lastname}")
        else:
            print("No patients assigned to this fitness expert.")
    else:
        print("Fitness expert not found.")

# Main function to allow the option to register and view users' details
def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            print("1. Register a doctor")
            print("2. View doctor details")
            doctor_choice = input("Enter your choice: ")
            if doctor_choice == '1':
                register_doctor()
            elif doctor_choice == '2':
                view_doctor_details()
            else:
                print("Invalid choice.")
        elif choice == '2':
            print("1. Register a patient")
            print("2. View patient details")
            patient_choice = input("Enter your choice: ")
            if patient_choice == '1':
                register_patient()
            elif patient_choice == '2':
                view_patient_details()
            else:
                print("Invalid choice.")
        elif choice == '3':
            print("1. Register a fitness expert")
            print("2. View fitness expert details")
            fitness_expert_choice = input("Enter your choice: ")
            if fitness_expert_choice == '1':
                register_fitness_expert()
            elif fitness_expert_choice == '2':
                view_fitness_expert_details()
            else:
                print("Invalid choice.")
        elif choice == '4':
            sys.exit("Exiting program.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
