from fastapi import HTTPException, status

MaxValueException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Товары такой стоимости мы не перевозим, извините.",
)

NoTariffPresent = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Прайса на заданное число или для такой категории товара нет.",
)

NonCorrectDeclaredValue = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Цена должна быть положительным числом.",
)

NonCorrectRateValue = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Цена должна быть задана числом",
)