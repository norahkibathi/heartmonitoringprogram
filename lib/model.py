#the purpose of the code is to allow users to manage a system that allows users to monitor their heart failure risk
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class Specialist(Base):
    __tablename__ = 'specialists'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    specialization = Column(String)
    patients_assigned = relationship("Patient", back_populates="assigned_specialist", foreign_keys="[Patient.specialist_id]")

    def __init__(self, firstname, lastname, age, gender,  specialization):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.specialization = specialization
        
        

  

    def consult(self, patient):
     if patient.risk_category.startswith("HIGH RISK"):
        return f"Cardiologist {self.firstname} {self.lastname} is ready to consult with {patient.firstname} {patient.lastname}."
     elif patient.risk_category.startswith("MODERATE RISK"):
        return f"General Doctor {self.firstname} {self.lastname} is ready to consult with {patient.firstname} {patient.lastname}."
     else:
        return f"Nurse {self.firstname} {self.lastname} will assist {patient.firstname} {patient.lastname}."

 
   
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    diabetes = Column(Boolean)
    family_history = Column(Boolean)
    hypertension = Column(Boolean)
    weight = Column(Float)
    height = Column(Float)
    smoking = Column(Boolean)
    heart_failure = Column(Boolean)
    cholesterol_level = Column(String)  # Add cholesterol level
    heart_rate = Column(Integer)  # Add heart rate
    blood_pressure = Column(String)  # Add blood pressure
    ecg_results = Column(String)  # Add ECG results
    risk_score = Column(Integer)
    risk_category = Column(String)
    specialist_id = Column(Integer, ForeignKey('specialists.id'))  
    assigned_specialist = relationship("Specialist", back_populates="patients_assigned", foreign_keys="[Patient.specialist_id]")

    def __init__(self, firstname, lastname, age, gender, diabetes=False, hypertension=False, smoking=False, weight=0.0, height=0.0,
                 family_history=False, heart_failure=False, cholesterol_level=None, heart_rate=None, blood_pressure=None, ecg_results=None):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.diabetes = diabetes
        self.hypertension = hypertension
        self.smoking = smoking
        self.weight = weight
        self.height = height
        self.heart_failure = heart_failure
        self.family_history = family_history
        self.cholesterol_level = cholesterol_level  # Initialize cholesterol level
        self.heart_rate = heart_rate  # Initialize heart rate
        self.blood_pressure = blood_pressure  # Initialize blood pressure
        self.ecg_results = ecg_results  # Initialize ECG results
        self.calculate_risk_score()
        self.get_risk_category()


#the framework of the app enables calculation of risk
    def calculate_risk_score(self):
        
        self.risk_score = int(self.age >= 65) + int(self.diabetes) + int(self.hypertension) + int(self.smoking)
        if self.weight:
            bmi = self.weight / ((self.height / 100) ** 2)
            if bmi < 18.5 or bmi >= 25:
                self.risk_score += 1
        self.risk_score += int(self.family_history) + int(self.heart_failure)

        # Adjust based on cholesterol level
        if self.cholesterol_level and self.cholesterol_level =="High":  # Assuming cholesterol_level is in mg/dL
            self.risk_score += 1

        # Adjust based on heart rate
        if self.heart_rate:
            if self.gender == "Male":
                if self.heart_rate > 100:  # High heart rate threshold for males
                    self.risk_score += 1
            else:
                if self.heart_rate > 90:  # High heart rate threshold for females
                    self.risk_score += 1

        # Adjust based on blood pressure
        if self.blood_pressure:
            systolic, diastolic = map(int, self.blood_pressure.split("/"))
            if systolic >= 140 or diastolic >= 90:  # High blood pressure threshold
                self.risk_score += 1

        # Adjust based on ECG results
        if self.ecg_results == "Abnormal":
            self.risk_score += 1

        self.get_risk_category()

    
#enables direction whether to visit an expert or not
    def get_risk_category(self):
       if self.risk_score >= 4:
            self.risk_category = "HIGH RISK: Please consult a cardiologist for further evaluation and management."
       elif self.risk_score >= 2:
            self.risk_category = "MODERATE RISK: Consider lifestyle modifications and consult a general doctor for advice."
       else:
            self.risk_category = "LOW RISK: Maintain healthy habits and schedule regular checkups."


DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
