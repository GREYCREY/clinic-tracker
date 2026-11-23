from dataclasses import dataclass, field
from datetime import date

from clinic.exceptions import ValidationError


@dataclass
class Prescription:
    drug: str
    dose_mg: float
    prescribed_at: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if not self.drug.strip() or self.dose_mg <= 0:
            raise ValidationError("Неверные данные медикамента")

    @property
    def dose_g(self) -> float:
        return self.dose_mg / 1000

