from datetime import date
from typing import Optional

from pydantic import BaseModel
from tortoise import fields, Model


class Tariff(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(index=True)
    cargo_type = fields.CharField(max_length=50, index=True)
    rate = fields.FloatField()

    @classmethod
    async def get_rate(
        cls, current_date: date, cargo_type: str
    ) -> Optional[float]:
        tariff = await cls.filter(
            date=current_date, cargo_type=cargo_type
        ).first()
        return tariff.rate


class InsuredValue(BaseModel):
    declared_value: float


class InsuranceCost(BaseModel):
    cargo_type: str
    current_date: date
    declared_value: float
    insurance_cost: Optional[float]
