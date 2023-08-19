from aiogram import Bot, Dispatcher,  types

# Получение токена бота
TOKEN = '5575568139:AAEuNC2x_yW23LFcefoBmmsc7AZw31abqyA'

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик входящих сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    # Обработка ссылки
    if message.entities and message.entities[0].type == 'url':
        url = message.text
        await handle_url(url)

    # Отправка ответа на сообщение
    await message.answer('Спасибо за сообщение!')

# Обработка ссылки
async def handle_url(url: str):
    pass
    # Реализация перехода по ссылке
    # В этой функции можно выполнить любые действия с полученной ссылкой
    # Например, получить данные с внешнего ресурса и отправить пользователю информацию

# Запуск бота
if __name__ == '__main__':
    dp.start_polling(dp)