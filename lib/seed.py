from faker import Faker
from model import Doctor, Patient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a Faker instance
fake = Faker()

# Define function to generate fake data for doctors
def generate_doctor_data():
    return {
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'age': fake.random_int(min=25, max=70),
        'gender': fake.random_element(elements=('male', 'female')),
        'address': fake.address(),
        'email': fake.email(),

        'phone_number': fake.phone_number(),
        'salary': fake.random_int(min=5000, max=15000),
        'working_hours': fake.random_int(min=20, max=40)
    }

# Define function to generate fake data for patients
def generate_patient_data():
    return {
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'age': fake.random_int(min=18, max=90),
        'gender': fake.random_element(elements=('male', 'female')),
        'address': fake.address(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'diabetes': fake.boolean(),
        'hypertension': fake.boolean(),
        'smoking': fake.boolean(),
        'family_history': fake.boolean(),
        'heart_failure': fake.boolean(),
        'weight': fake.random_int(min=40, max=150),
        'height': fake.random_int(min=140, max=200)
    }



# Create engine and session
DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Generate and insert fake data for doctors
for _ in range(10):  # Generate 10 doctors
    doctor_data = generate_doctor_data()
    doctor = Doctor(**doctor_data)
    session.add(doctor)

# Generate and insert fake data for patients
for _ in range(20):  # Generate 20 patients
    patient_data = generate_patient_data()
    patient = Patient(**patient_data)
    session.add(patient)


# Commit the changes
session.commit()
