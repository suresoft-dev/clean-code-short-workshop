import math

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class TemperatureData:
    datetime: datetime
    value_in_kelvin: float

    @staticmethod
    def from_csv(csv: str) -> "TemperatureData":
        dt, kelvin = csv.split(",")
        return TemperatureData(datetime.fromisoformat(dt), float(kelvin))


INPUT_FILE = Path("values.csv")
RESULT_FILE = Path("logfile.txt")


def read_temperature_data(path: Path) -> list[TemperatureData]:
    return [TemperatureData.from_csv(line) for line in path.read_text().splitlines()]


def is_valid_value(d: TemperatureData) -> bool:
    return not math.isnan(d.value_in_kelvin)


def is_in_timeframe(d: TemperatureData, start: datetime, end: datetime) -> bool:
    return start < d.datetime < end


def celsius(d: TemperatureData) -> float:
    return d.value_in_kelvin - 273.15


def celsius_values_in_timeframe(
    data: list[TemperatureData], start: datetime, end: datetime
) -> list[float]:
    return [
        celsius(d) for d in data if is_valid_value(d) and is_in_timeframe(d, start, end)
    ]


def write_results(result_file: Path, values: list[float]) -> None:
    result_file.write_text("\n".join(map(str, values)))


START_DATE = datetime(2023, 9, 20, hour=8)
END_DATE = START_DATE + timedelta(hours=2)

if __name__ == "__main__":
    data = read_temperature_data(INPUT_FILE)
    celsius_values = celsius_values_in_timeframe(data, START_DATE, END_DATE)
    write_results(RESULT_FILE, celsius_values)
