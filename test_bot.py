import LavaAPI
import time
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import Base
from aiogram import filters as F

token = "5932927143:AAFC-jMkcjAZp6i7yN4lz9AVTi4ohgRToVw"

lavaapi_key = "ключ от кошеля"
# lava_api = LavaAPI(lavaapi_key)
lava_api = 3

bot = Bot(token = token)
dp = Dispatcher(bot, storage = MemoryStorage())

class User_States(StatesGroup):
    main = State()
    buy = State()
    choice = State()
    product1 = State()
    product2 = State()

class Product():
    def __init__(self, price, name, LAVA_url, description, state):
        self.price = price
        self.name = name
        self.description = description
        self.LAVA_url = LAVA_url
        self.cash_check()
        self.state = state
    def cash_check():
        # вставляете сюда свой код для проверки наличия на складе, пока что пусто и товар всегда есть
        return 

class Pr1(Product):
    pass

class Pr2(Product):
    pass

Pr2.price = 1000
Pr2.name = "Товар 2 | " + str(Pr2.price) + " RUB"
Pr2.description = "Крайне хороший товар"
Pr2.LAVA_url = "https://lava.ru/dashboard"
Pr2.state = User_States.product2

Pr1.price = 500
Pr1.name = 'Товар | ' + str(Pr1.price) + ' RUB'
Pr1.description = "Хороший товар"
Pr1.LAVA_url = "https://lava.ru/dashboard"
Pr1.state = User_States.product1

all_but = [Pr1, Pr2]
all_name = [Pr1.name, Pr2.name]
all_price = ["Купить за " + str(Pr1.price) + " RUB", "Купить за " + str(Pr2.price) + " RUB"]

@dp.message_handler(commands = ("start"))
async def start(message: types.Message):
    Base.add_id(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    but2 = types.KeyboardButton(text = "Купить")
    keyboard.add(but2)
    await User_States.main.set()
    await bot.send_message(message.chat.id, text = "Привет я такой-то такой-то бот для продажи нитро", reply_markup = keyboard)

@dp.message_handler(Text(equals = "Купить"), state = User_States.main)
async def buy(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for i in all_but:
        keyboard.add(types.KeyboardButton(text = i.name))
    await User_States.buy.set()
    await bot.send_message(message.chat.id, text = "Что вы хотите купить?", reply_markup = keyboard)

@dp.message_handler(lambda message: message.text in all_name, state = User_States.buy)
async def what_buy(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for i in all_but:
        if message.text == i.name:
            but = types.InlineKeyboardButton(text = "Купить за " + str(i.price) + " RUB", callback_data = str(i.price))
            if i.state == User_States.product1:
                await User_States.product1.set()
            else:
                await User_States.product2.set()
            break
    keyboard.add(but)
    await bot.send_message(message.chat.id, text = i.description, reply_markup = keyboard)

@dp.callback_query_handler(state = User_States.product1)
async def sell_product1(callback: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True).add(types.KeyboardButton(text = "Проверить"), types.KeyboardButton(text = "Отмена"))
    keyboard_2 = types.InlineKeyboardMarkup.add(types.InlineKeyboardButton(text = "Оплатить", url = Pr1.LAVA_url))
    Base.change_time(callback.message.chat.id, time.time())
    await callback.message.answer("Цена 500\nВремя на отпраку денег - 7 минут. Время пошло", reply_markup = keyboard_2)
    await User_States.choice.set()
    await callback.message.answer("Если вы перевели деньги, нажмите кнопку «проверить»", reply_markup = keyboard)

@dp.callback_query_handler(state = User_States.product2)
async def sell_product1(callback: types.CallbackQuery):
    print(1)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True).add(types.KeyboardButton(text = "Проверить"), types.KeyboardButton(text = "Отмена"))
    keyboard_2 = types.InlineKeyboardMarkup.add(types.InlineKeyboardButton(text = "Оплатить", url = Pr2.LAVA_url))
    Base.change_time(callback.message.chat.id, time.time())
    await callback.message.answer("Цена 500\nВремя на отпраку денег - 7 минут. Время пошло", reply_markup = keyboard_2)
    await User_States.choice.set()
    await callback.message.answer("Если вы перевели деньги, нажмите кнопку «проверить»", reply_markup = keyboard)

@dp.message_handler(Text(equals = "Проверить"), state = User_States.choice)
async def cancel(message: types.Message):
    if time.time() - Base.get(message.chat.id) > 60*7:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        but1 = types.KeyboardButton(text = "Купить")
        keyboard.add(but1)
        await User_States.main.set()
        await bot.send_message(message.chat.id, text = "К сожелению прошло больше 7 минут, возвращаю вас в главное меню", reply_markup = keyboard)
    elif lava_api.create_invoice(500, "text").is_paid():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        but1 = types.KeyboardButton(text = "Купить")
        keyboard.add(but1)
        await User_States.main.set()
        await bot.send_message(message.chat.id, text = "Спасибо за покупку вот ваш товар\nВозвращаю в главное меню", reply_markup = keyboard)
    else:
        await bot.send_message(message.chat.id, text = "Оплата не прошла, попробуйте ещё раз", reply_markup = keyboard)

@dp.message_handler(Text, state = "*")
async def check_balance(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    but1 = types.KeyboardButton(text = "Купить")
    keyboard.add(but1)
    await User_States.main.set()
    await bot.send_message(message.chat.id, text = "Возвращаюсь в главное меню", reply_markup = keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup = print("Запуск"))