from dataclasses import dataclass, field
from datetime import date, today
from typing import Self, Any
from clinic.exceptions import ValidationError


@dataclass
class Prescription:
    drug: str
    dose_mg: float
    prescribed_at: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if not self.drug.strip():
            raise ValidationError("Неверные данные медикамента")
        if self.dose_mg <= 0:
            raise ValidationError(f"Доза должна быть положительной: {self.dose_mg}")
    @property
    def dose_g(self) -> float:
        return self.dose_mg / 1000
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            drug=data["drug"],
            dose_mg=float(data["dose_mg"]),
            prescribed_at=date.fromisoformat(data["prescribed_at"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"drug": f"{self.drug}", "dose_mg": f"{self.dose_mg}", "prescribed_at": f"{self.prescribed_at.isoformat()}"}
    
@dataclass
class Patient:
    policy: str
    name: str = field(compare=False)
    birth_date: date = field(compare=False)
    prescriptions: list[Prescription] = field(default_factory=list, compare=False)
    def __post_init__(self) -> None:
            if not self.policy.isdigit():
                            raise ValidationError("Полис должен содержать только цифры")
            if not self.name.strip():
                raise ValidationError("Имя не может быть пустым")
            if self.birth_date <= today().date():
                raise ValidationError(f"Дата рождения не может быть в будущем: {self.birth_date}")

    def add_prescroption(self, prescripton: Prescription) -> None:
        self.prescriptions.append(prescripton)
        
    @property
    def age(self) -> int:
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        
        return int(age)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            policy=data["policy"],
            name=data["name"],
            birth_date=date.fromisoformat(data["birth_date"]),
            prescriptions=data["prescriptions"]
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {"policy": f"{self.policy}", "name": f"{self.name}", "birth_date": f"{self.birth_date.isoformat()}", "prescriptions": f"{self.prescriptions}"}