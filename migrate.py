import os

from dotenv import load_dotenv
from tortoise import run_async, Tortoise

load_dotenv("infra/.env")


async def main():
    await Tortoise.init(
        db_url=os.getenv("DB_URL"),
        modules={"models": ["main"]},
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(main())
