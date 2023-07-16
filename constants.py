from pydantic import condecimal

MAX_LENGTH_CARGO_TYPE_NAME = 50
MONEY = condecimal(gt=0, decimal_places=2)
MAX_DIGITS_IN_RATE = 5
MAX_DECIMAL_PLACES_IN_RATE = 2
MAX_PRODUCT_PRICE: MONEY = 10000000
