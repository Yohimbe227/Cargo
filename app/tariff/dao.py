from datetime import date

from app.tariff.models import Tariff


class TariffDAO:
    model = Tariff

    @classmethod
    async def create(cls, cargo_date: date, rate: float, cargo_type: str):
        tariff = await cls.model.create(
            date=cargo_date, rate=rate, cargo_type=cargo_type
        )
        return tariff

    @classmethod
    async def get_rate(cls, current_date: date, cargo_type: str):
        tariff = await cls.model.filter(
            date=current_date, cargo_type=cargo_type
        ).first()
        print(tariff, current_date, cargo_type)
        if tariff:
            return tariff.rate

    @classmethod
    async def get(cls, tariff_date: date, cargo_type: str):
        tariff = await cls.model.get_or_none(
            date=tariff_date, cargo_type=cargo_type
        )
        return tariff
