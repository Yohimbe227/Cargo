from fastapi import HTTPException, status

MaxValueException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Товары такой стоимости мы не перевозим, извините.",
)

NoTariffPresentException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Прайса на заданное число или для такой категории товара нет.",
)

NonCorrectDeclaredValueException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Цена должна быть положительным числом.",
)

NoTariffException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Пустой запрос. Введите тариф.",
)


class InvalidRateValueExceptions(HTTPException):
    def __init__(self, rate):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Значение {rate} должно быть числом в пределах от 0 до 1!",
        )


class InvalidDateFormatException(HTTPException):
    def __init__(self, date_str):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Invalid date format: {date_str}",
        )
