from datetime import date, datetime
from decimal import Decimal

from fastapi import FastAPI, status, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.transactions import in_transaction

from app.tariff.dao import TariffDAO
from app.tariff.models import InsuranceCost, InsuredValue, Tariff
from exceptions import NonCorrectRateValue

app = FastAPI()


@app.post("/calculate_insurance_cost", response_model=InsuranceCost)
async def calculate_insurance_cost(
    insured_value: InsuredValue,
    cargo_type: str,
    current_date: date = datetime.utcnow().date(),
) -> InsuranceCost:
    declared_value = insured_value.declared_cost
    rate = await Tariff.get_rate(current_date, cargo_type)
    insurance_cost = Decimal(str(rate)) * declared_value if rate else None

    return InsuranceCost(
        cargo_type="Other",
        current_date=current_date,
        declared_value=declared_value,
        insurance_cost=insurance_cost,
    )


@app.post("/tariffs")
async def add_or_update_tariffs(tariff_data: list[dict]):
    async with in_transaction():
        for data in tariff_data:
            date_str = data["date"]
            tariffs = data["tariffs"]
            try:
                tariff_date = date.fromisoformat(date_str)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"Invalid date format: {date_str}",
                )
            for tariff in tariffs:
                try:
                    rate = float(tariff.get("rate"))
                except ValueError:
                    raise NonCorrectRateValue
                if rate is None or rate < 0 or rate > 1:
                    raise HTTPException(
                        status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail=f"Значение {rate} должно быть числом в "
                        f"пределах от 0 до 1!",
                    )
                existing_tariff = await TariffDAO.get(
                    date=tariff_date, cargo_type=tariff["cargo_type"]
                )
                if existing_tariff:
                    existing_tariff.rate = tariff["rate"]
                    await existing_tariff.save()
                else:
                    await TariffDAO.create(
                        date=tariff_date,
                        cargo_type=tariff["cargo_type"],
                        rate=tariff["rate"],
                    )
    return {"message": "Тариф успешно добавлен"}

register_tortoise(
    app,
    db_url="postgres://postgres:4130@db:5432/postgres",
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
