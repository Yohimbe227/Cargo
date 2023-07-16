import json
from main import Tariff

with open("tariff.json", "r") as file:
    data = json.load(file)

for date, tariffs in data.items():
    for tariff_data in tariffs:
        Tariff.create(
            date=date,
            cargo_type=tariff_data["cargo_type"],
            rate=tariff_data["rate"],
        )
