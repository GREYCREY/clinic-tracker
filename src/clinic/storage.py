import json
from abc import ABC, abstractmethod
from pathlib import Path

from clinic.exceptions import StorageError, ValidationError
from clinic.models import Patient


class Storage(ABC):

    @abstractmethod
    def load(self)-> dict[str, Patient]:
        pass

    @abstractmethod
    def save(self,patients: dict[str, Patient]) -> None:
        pass

class JsonStorage(Storage):
    def __init__(self, path: Path):
        self.path = path
    
    def load(self) -> dict[str, Patient]:
        if self.path.exists():
            try:
                with open (f'{self.path}', encoding='utf-8') as json_file:
                    parsed_data = json.load(json_file)
                    patients = {}
                    for policy, patient_data in parsed_data.items():
                        patient = Patient.from_dict(patient_data)
                        patients[policy] = patient
                    return patients
            except (
                OSError,
                json.JSONDecodeError,
                KeyError,
                ValueError,
                ValidationError,
                ) as e:
                raise StorageError("Ошибка при загрузке JSON") from e
        else:
            return {}

    def save(self, patients: dict[str, Patient]) -> None:
        data_for_save = {}
        for policy, patient_data in patients.items():
            patient_to_dict = patient_data.to_dict()
            data_for_save[policy] = patient_to_dict
        try:
            with open (self.path, 'w', encoding="utf-8") as json_file:
                json.dump(
                    data_for_save,
                    json_file,
                    ensure_ascii=False,
                    indent=2
                    )
        except(
            OSError,
            json.JSONDecodeError,
            KeyError,
            ValueError,
            ValidationError,
        ) as e:
            raise StorageError("Ошибка при сохранении JSON") from e
