from datetime import date

from app.tariff.models import Tariff


class TariffDAO:
    model = Tariff

    @classmethod
    async def create(cls, date: date, cargo_type: str, rate: float):
        await cls.model.create(date=date, cargo_type=cargo_type, rate=rate)

    @classmethod
    async def get(cls, date: date, cargo_type: str):
        tariff = await cls.model.get_or_none(date=date, cargo_type=cargo_type)
        return tariff
