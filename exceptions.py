from fastapi import HTTPException, status

MaxValueException = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Товары такой стоимости мы не перевозим, извините.",
)
