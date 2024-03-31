import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Doctor, Patient

DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine('sqlite:///heart.db')
Session = sessionmaker(bind=engine)
session = Session()

# the function enables the user to interact with display menu function
def display_menu():
    print("Welcome to the Heart Health Management System")
    print("1. Manage Doctors")
    print("2. Manage Patients")
    print("3. Exit")

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
            sys.exit("Exiting program.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
