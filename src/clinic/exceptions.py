class ClinicError(Exception):
    """Базовое исключение приложения."""


class ValidationError(ClinicError):
    """Некорректные входные данные."""


class PatientNotFoundError(ClinicError):
    def __init__(self, policy: str) -> None:
        super().__init__(f"Пациент с полисом {policy} не найден")
        self.policy = policy


class DuplicatePatientError(ClinicError):
    def __init__(self, policy: str) -> None:
        super().__init__(f"Пациент с полисом {policy} уже существует")
        self.policy = policy


class StorageError(ClinicError):
    """Ошибка хранилища."""
