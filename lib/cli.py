import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Specialist, Patient

DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine('sqlite:///heart.db')
Session = sessionmaker(bind=engine)
session = Session()

def display_menu():
    print("Welcome to the Heart Health Management System")
    print("1. Manage Specialists")
    print("2. Manage Patients")
    print("3. Exit")

def register_specialist():
    print("Register a Specialist")
    firstname = input("Enter specialist's first name: ")
    lastname = input("Enter specialist's last name: ")
    age = int(input("Enter specialist's age: "))
    gender = input("Enter specialist's gender: ")
    specialization = input("Enter specialist's specialization (Cardiologist/General Doctor/Nurse): ")
    specialist = Specialist(firstname=firstname, lastname=lastname, age=age, gender=gender, specialization=specialization)
    session.add(specialist)
    session.commit()
    print("Specialist registered successfully!")

def view_specialist_details():
    specialist_id = int(input("Enter specialist's ID: "))
    specialist = session.query(Specialist).filter(Specialist.id == specialist_id).first()
    if specialist:
        print("Specialist Details:")
        print(f"Name: {specialist.firstname} {specialist.lastname}")
        print(f"Age: {specialist.age}")
        print(f"Gender: {specialist.gender}")
        print(f"Specialization: {specialist.specialization}")
    else:
        print("Specialist not found.")

def register_patient():
    print("Register a Patient")
    firstname = input("Enter patient's first name: ")
    lastname = input("Enter patient's last name: ")
    age = int(input("Enter patient's age: "))
    gender = input("Enter patient's gender: ")
    diabetes = input("Does the patient have diabetes? (True/False): ").lower() == 'true'
    hypertension = input("Does the patient have hypertension? (True/False): ").lower() == 'true'
    smoking = input("Is the patient a smoker? (True/False): ").lower() == 'true'
    family_history = input("Does the patient have a family history of heart disease? (True/False): ").lower() == 'true'
    heart_failure = input("Has the patient experienced heart failure before? (True/False): ").lower() == 'true'
    cholesterol_level = input("Enter patient's cholesterol level (High/Normal/Low): ")
    heart_rate = int(input("Enter patient's heart rate in beats per minute: "))
    blood_pressure = input("Enter patient's blood pressure (systolic/diastolic): ")
    ecg_results = input("Enter patient's ECG results (Normal/Abnormal): ")

    weight_input = input("Enter patient's weight in kg (optional, press Enter to skip): ")
    height_input = input("Enter patient's height in cm (optional, press Enter to skip): ")

    weight = float(weight_input) if weight_input else None
    height = float(height_input) if height_input else None

    patient = Patient(firstname=firstname, lastname=lastname, age=age, gender=gender,
                      diabetes=diabetes, hypertension=hypertension, smoking=smoking,
                      family_history=family_history, heart_failure=heart_failure,
                      weight=weight, height=height,
                      cholesterol_level=cholesterol_level, heart_rate=heart_rate,
                      blood_pressure=blood_pressure, ecg_results=ecg_results)

    patient.calculate_risk_score()
    patient.get_risk_category()

    session.add(patient)
    session.commit()

    print("Patient registered successfully!")

def view_patient_details():
    patient_id = int(input("Enter patient's ID: "))
    patient = session.query(Patient).filter(Patient.id == patient_id).first()

    if patient:
        print("Patient Details:")
        print(f"Name: {patient.firstname} {patient.lastname}")
        print(f"Age: {patient.age}")
        print(f"Gender: {patient.gender}")
        print(f"Diabetes: {patient.diabetes}")
        print(f"Hypertension: {patient.hypertension}")
        print(f"Risk Score: {patient.risk_score}")
        print(f"Risk Category: {patient.risk_category}")
        if patient.specialist:
            print("Assigned Specialist:")
            print(f"- {patient.specialist.firstname} {patient.specialist.lastname}")
        else:
            print("No specialist assigned to this patient.")
    else:
        print("Patient not found.")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            print("1. Register a specialist")
            print("2. View specialist details")
            specialist_choice = input("Enter your choice: ")
            if specialist_choice == '1':
                register_specialist()
            elif specialist_choice == '2':
                view_specialist_details()
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
            sys.exit("Exiting program.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
