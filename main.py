import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db
from handlers import start, help, about, services, projects, contact, text, shop, cart


async def main():
    # Инициализируем базу данных
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем все роутеры
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(about.router)
    dp.include_router(services.router)
    dp.include_router(projects.router)
    dp.include_router(contact.router)
    dp.include_router(shop.router)
    dp.include_router(cart.router)  # <-- добавили
    dp.include_router(text.router)

    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
