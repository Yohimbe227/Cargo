# from datetime import date
#
# from fastapi import APIRouter, Request, Depends
#
# from app.tariff.dao import BookingDAO
# from app.bookings.schemas import SBooking
# from app.exceptions import RoomCannotBeBooked
# from app.users.dependencies import get_current_user
# from app.users.models import Users
#
# router = APIRouter(
#     prefix="/tariff",
#     tags=["tariff"],
# )
#
#
# # @router.get("")
# # async def get_tariff(user: Users = Depends(get_current_user)) -> list[SBooking]:
# #     return await BookingDAO.find_all(user_id=user.id)
#
#
# @router.post("")
# async def add_tariff(
#     cargo_type: int,
#     date: date,
#     rate: date,
#     # user: Users = Depends(get_current_user),
# ):
#     booking = await BookingDAO.add(rate, cargo_type, date)
#     if not booking:
#         raise RoomCannotBeBooked
