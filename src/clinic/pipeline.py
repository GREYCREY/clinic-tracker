import logging
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from clinic.exceptions import StorageError, ValidationError
from clinic.models import Prescription

logger = logging.getLogger(__name__)


@dataclass
class ImportResult:
    imported: int = 0
    skipped: int = 0


def read_lines(path: Path) -> Iterator[str]:
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                yield line.strip()
    except OSError as e:
        raise StorageError(f"Возникла ошибка: {e}, при чтении файла {path}") from e


def parse_lines(
    lines: Iterable[str], result: ImportResult
) -> Iterator[tuple[str, Prescription]]:
    for line_no, line in enumerate(lines, start=1):
        if not line:
            logger.warning("Строка %d пропущена: пустая", line_no)
            result.skipped += 1
            continue

        fields = [field.strip() for field in line.split(";")]
        if len(fields) != 3:
            logger.warning("Строка '%d' пропущена: ожидалось 3 поля", line_no)
            result.skipped += 1
            continue

        policy, drug, dose = fields
        try:
            prescription = Prescription(drug, float(dose))
        except (ValueError, ValidationError) as e:
            logger.warning("Cтрока '%d' пропущена: %s", line_no, e)
            result.skipped += 1
            continue

        yield policy, prescription
