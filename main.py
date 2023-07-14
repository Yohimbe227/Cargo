from datetime import date, time

from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.transactions import in_transaction

from app.tariff.dao import TariffDAO
from app.tariff.models import InsuranceCost, InsuredValue, Tariff

app = FastAPI()


@app.post("/calculate_insurance_cost", response_model=InsuranceCost)
async def calculate_insurance_cost(
    insured_value: InsuredValue, current_date: date = date.today()
):
    declared_value = insured_value.declared_value

    rate = await Tariff.get_rate(current_date, "Other")
    insurance_cost = declared_value * rate if rate else None

    return InsuranceCost(
        cargo_type="Other",
        date=current_date,
        declared_value=declared_value,
        insurance_cost=insurance_cost,
    )


@app.post("/tariffs")
async def add_or_update_tariffs(tariff_data: dict):
    async with in_transaction():
        for date_str, tariffs in tariff_data.items():
            tariff_date = date_str.utcnow().date()
            for tariff in tariffs:
                existing_tariff = await TariffDAO.get(
                    tariff_date=tariff_date, cargo_type=tariff["cargo_type"]
                )
                if existing_tariff:
                    existing_tariff.rate = tariff["rate"]
                    await existing_tariff.save()
                else:
                    await TariffDAO.create(
                        cargo_date=tariff_date,
                        cargo_type=tariff["cargo_type"],
                        rate=tariff["rate"],
                    )

    return {"message": "Тариф успешно добавлен"}


class Order(BaseModel):
    cargo_type: str
    declared_value: float
    date_order: time


register_tortoise(
    app,
    db_url="postgres://postgres:4130@localhost:5432/cargo",
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
