import os
from datetime import date, datetime
from decimal import Decimal

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.transactions import in_transaction

from app.tariff.dao import TariffDAO
from app.tariff.models import InsuranceCost, InsuredValue, Tariff
from exceptions import (
    NoTariffException,
    InvalidRateValueExceptions,
    InvalidDateFormatException,
)

load_dotenv("infra/.env.local")
app = FastAPI()


@app.post("/calculate_insurance_cost", response_model=InsuranceCost)
async def calculate_insurance_cost(
        insured_value: InsuredValue,
        cargo_type: str,
        insuarance_date: date = datetime.utcnow().date(),
) -> InsuranceCost:
    """Расчет стоимости страховки.

    Args:
        insured_value: Объявленная стоимость.
        cargo_type: Тип груза.
        insuarance_date: Дата страхования.

    Returns:
        Стоимость страхования в зависимости от тарифа и параметров груза.

    """

    declared_value = insured_value.declared_cost
    rate = await Tariff.get_rate(insuarance_date, cargo_type)
    insurance_cost = Decimal(str(rate)) * declared_value if rate else None

    return InsuranceCost(
        cargo_type="Other",
        current_date=insuarance_date,
        declared_value=declared_value,
        insurance_cost=insurance_cost,
    )


@app.post("/tariffs")
async def add_or_update_tariffs(
        tariff_data: dict[str, list[dict[str, str | float]]]
) -> dict[str, str]:
    """Добавление тарифа в базу данных.

    Args:
        tariff_data: данные тарифа в формате json.

    Returns:
        Сообщение об успешно завершении добавлении тарифа, либо ошибка,
        отсылаемая пользователю.

    Raises:
        InvalidDateFormatException: Неверный формат даты.
        InvalidRateValueExceptions: Некорректное значение коэффициента `rate`.
    Должно быть от 0 до 1 и должно быть числом.

    """
    if not tariff_data:
        raise NoTariffException
    async with in_transaction():
        for date_str, tariffs in tariff_data.items():
            try:
                tariff_date = date.fromisoformat(date_str)
            except ValueError:
                raise InvalidDateFormatException(date_str)
            for tariff in tariffs:
                try:
                    rate = float(tariff.get("rate"))
                except ValueError:
                    raise InvalidRateValueExceptions(rate)
                if rate is None or rate < 0 or rate > 1:
                    raise InvalidRateValueExceptions(rate)
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
    db_url=os.getenv("DB_URL"),
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
