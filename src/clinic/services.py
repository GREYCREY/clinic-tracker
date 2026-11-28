from clinic.storage import Storage
from clinic.models import Prescription, Patient
from clinic.pipeline import ImportResult
from clinic.exceptions import DuplicatePatientError, PatientNotFoundError
from datetime import date
from pathlib import Path

class ClinicService:
    def __init__(self, storage: Storage ) -> None:
        self.storage = storage
        
    def add_patient(self, policy: str, name: str, birth_date: date) -> Patient:
        patients = self.storage.load()
        if policy in patients:
            raise DuplicatePatientError("Пациент с таким полисом уже существует")
        patient = Patient(policy, name, birth_date)
        patients[policy] = patient
        self.storage.save(patients)
        return patient
    
    def get_patient(self, policy: str) -> Patient:
        patients = self.storage.load()
        if policy not in patients:
            raise PatientNotFoundError("Пациент с таким полисом отсутствует")
        return patients[policy]
    
    def list_patients(self) -> list[Patient]:
        patients_dict = self.storage.load()
        patients_list = list(patients_dict.values())
        patients_list_sorted = sorted(patients_list, key=lambda patient: patient.name)
        return patients_list_sorted
    
    def add_prescription(self, policy: str, drug: str, dose_mg: float) -> Prescription:
        patients = self.storage.load()
        if policy not in patients:
                    raise PatientNotFoundError("Пациент с таким полисом отсутствует")
        prescription = Prescription(drug, dose_mg)
        patients[policy].add_prescription(prescription)
        self.storage.save(patients)
        return prescription
    
    