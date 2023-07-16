from tortoise import run_async, Tortoise


async def main():
    await Tortoise.init(
        db_url="postgres://postgres:4130@localhost:5432/cargo",
        modules={"models": ["main"]},
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(main())
