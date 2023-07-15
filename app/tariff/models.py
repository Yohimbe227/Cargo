from datetime import date

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
from exceptions import MaxValueException


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
    def validate_date(cls, value):
        if value > MAX_PRODUCT_PRICE:
            raise MaxValueException
        return round(value, 2) if value is not None else None

    @classmethod
    async def get_rate(
        cls, current_date: date, cargo_type: str
    ) -> MONEY | None:
        tariff = await cls.filter(
            date=current_date, cargo_type=cargo_type
        ).first()
        if tariff:
            return tariff.rate


class InsuredValue(BaseModel):
    declared_cost: MONEY


class InsuranceCost(BaseModel):
    cargo_type: str
    current_date: date | None
    declared_value: MONEY
    insurance_cost: MONEY | None

    @validator("insurance_cost", pre=True)
    def round_insurance_cost(cls, value):
        if value > MAX_PRODUCT_PRICE:
            raise MaxValueException
        return round(value, 2) if value is not None else None
