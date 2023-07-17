from datetime import date
from decimal import Decimal

from pydantic import BaseModel, validator
from tortoise import fields, Model
from tortoise.validators import MaxValueValidator, MinValueValidator

from constants import (
    MAX_LENGTH_CARGO_TYPE_NAME,
    MONEY,
    MAX_DECIMAL_PLACES_IN_RATE,
    MAX_DIGITS_IN_RATE,
    MAX_PRODUCT_PRICE,
)
from exceptions import (
    MaxValueException,
    NoTariffPresentException,
    NonCorrectDeclaredValueException,
)


class Tariff(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(index=True)
    cargo_type = fields.CharField(
        max_length=MAX_LENGTH_CARGO_TYPE_NAME, index=True
    )
    rate = fields.DecimalField(
        max_digits=MAX_DIGITS_IN_RATE,
        decimal_places=MAX_DECIMAL_PLACES_IN_RATE,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )

    @validator("insurance_cost", pre=True)
    def validate_cost(cls, value):
        """Выдаем сообщение, если цена товара превышает `MAX_PRODUCT_PRICE`.

        Округляем введеное значения до двух знаков после запятой.
        Args:
            value: Задаваемая пользователем цена товара.

        Returns:
            Валидированная цена товара (округлени до сотых).

        """
        if value > MAX_PRODUCT_PRICE:
            raise MaxValueException
        return round(value, 2) if value is not None else None

    @classmethod
    async def get_rate(
        cls, current_date: date, cargo_type: str
    ) -> MONEY | None:
        """Получаем кэффициент `rate` для рассчета стоимости страхования.
        Args:
            current_date: Дата для расчета `rate`.
            cargo_type: Тип груза (необходим для расчета).
        Returns:
            Коэффициент `rate`.

        """
        tariff = await cls.filter(
            date=current_date, cargo_type=cargo_type
        ).first()
        if tariff:
            return float(tariff.rate)


class InsuredValue(BaseModel):
    """Модель объявленной стоимости груза."""

    declared_cost: MONEY


class InsuranceCost(BaseModel):
    """Модель стоимости страхования груза."""

    cargo_type: str
    current_date: date | None
    declared_value: MONEY
    insurance_cost: MONEY | None

    @validator("insurance_cost", pre=True)
    def round_insurance_cost(cls, value):
        """Валидация параметров тарифа.

        Args:
            value: Стоимость страхования.

        Returns:
            Округленное до 2-х знаков после запятой стоимость страхования.

        Raises:
            NoTariffPresentException: Если нет подходящего тарифа (по дате или
        виду груза)
            NonCorrectDeclaredValueException: Если не корректно заданна цена
        груза.

        """
        if value is None:
            raise NoTariffPresentException
        if value <= 0:
            raise NonCorrectDeclaredValueException
        if Decimal(value) > MAX_PRODUCT_PRICE:
            raise MaxValueException
        return round(value, 2) if value is not None else None
