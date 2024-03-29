#the purpose of the code is to allow users to manage a system that allows users to monitor their heart failure risk
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Doctor(Base):
    #the doctors are users or stakeholders of the systems with their different details log-in into the system
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True) #the primary key will allows creation of one to many relationship between the doctor and patient
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String)
    address = Column(String)
    phone_number = Column(String)
    working_hours = Column(Integer)
    salary = Column(Float, nullable=False)
    patients = relationship("Patient", backref="doctor")
#the function defines the attributes of the doctor
    def __init__(self, firstname, lastname, age, gender, address, email, phone_number, salary, working_hours=0):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.working_hours = working_hours
        self.salary = salary

    def calculate_salary(self):
        self.salary = 2000 * self.working_hours

    def consult(self, patient):
        if patient.risk_category.startswith("HIGH RISK") or patient.risk_category.startswith("MODERATE RISK"):
            return f"Doctor {self.firstname} {self.lastname} is ready to consult with {patient.firstname} {patient.lastname}."
        else:
            return f"Patient {patient.firstname} {patient.lastname} does not need a doctor's consultation at the moment."

class Patient(Base):
    #the data base collects demographics and health information to allow the patient to monitor their heart levels
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    diabetes = Column(Boolean)
    family_history = Column(Boolean)
    hypertension = Column(Boolean)
    weight = Column(Float)
    height = Column(Float)
    smoking = Column(Boolean)
    heart_failure = Column(Boolean)
    risk_score = Column(Integer)
    risk_category = Column(String)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))  #the foreign key enables relationship establsihment 
    fitness_expert_id = Column(Integer, ForeignKey('fitnessexperts.fitness_expert_id'))  
    doctor = relationship("Doctor", backref="patients")  
    fitness_expert = relationship("FitnessExpert", backref="patients")  

    def __init__(self, firstname, lastname, age, gender, address="", email="", phone="", diabetes=False, hypertension=False, smoking=False, weight=0.0, height=0.0,
                 family_history=False, heart_failure=False):
        #the attributes of the patient have been presented 
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.address = address
        self.email = email
        self.phone = phone
        self.diabetes = diabetes
        self.hypertension = hypertension
        self.smoking = smoking
        self.weight = weight
        self.height = height
        self.heart_failure = heart_failure
        self.family_history = family_history
        self.calculate_risk_score()
        self.get_risk_category()
#the framework of the app enables calculation of risk
    def calculate_risk_score(self):
        self.risk_score = int(self.age >= 65) + int(self.diabetes) + int(self.hypertension) + int(self.smoking)
        if self.weight:
            bmi = self.weight / ((self.height / 100) ** 2)
            if bmi < 18.5 or bmi >= 25:# the bmi was preffered as per WHO reccomendations
                self.risk_score += 1
        self.risk_score += int(self.family_history) + int(self.heart_failure)
#enables direction whether to visit an expert or not
    def get_risk_category(self):
        if self.risk_score >= 4:
            self.risk_category = "HIGH RISK: Please consult a doctor for further evaluation and management."
        elif self.risk_score >= 2:
            self.risk_category = "MODERATE RISK: Consider lifestyle modifications and consult a doctor for advice."
        else:
            self.risk_category = "LOW RISK: Maintain healthy habits and schedule regular checkups."

class FitnessExpert(Base):
    #fitness attributes with one to many relationship with the patient 
    __tablename__ = 'fitnessexperts'

    fitness_expert_id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    working_hours = Column(Integer)
    salary = Column(Float)
    patients = relationship("Patient", backref='fitness_expert')  

    def __init__(self, firstname, lastname, age, gender, address="", email="", phone_number="", working_hours=0, salary=None):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.working_hours = working_hours
        self.salary = self.calculate_salary(working_hours)

    def calculate_salary(self, working_hours):
        #an attempt to enhance the app
        base_salary = 1000.00
        hourly_rate = 50.00
        total_salary = base_salary + (working_hours * hourly_rate)
        return total_salary

    def consult(self, patient):
        #the code allocates different fitness experts with the patients
        if hasattr(patient, 'risk_category') and patient.risk_category.startswith("MODERATE RISK"):
            return f"Fitness expert {self.firstname} {self.lastname} is ready to consult with {patient.firstname} {patient.lastname}."
        else:
            return f"Patient {patient.firstname} {patient.lastname} does not need a fitness consultation at the moment."

DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
