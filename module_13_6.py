from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '8000769412:AAHrlLNLslcP0A3EeaGDD9bK7dXMvzukG_w'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.row(button, button2)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
in_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb2.add(in_button)
kb2.add(in_button2)


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup(resize_keyboard=True)
in_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb2 = InlineKeyboardMarkup(resize_keyboard=True)
in_button3 = InlineKeyboardButton(text='Мужской', callback_data='male')
in_button4 = InlineKeyboardButton(text='Женский', callback_data='female')
kb3 = InlineKeyboardMarkup(resize_keyboard=True)
in_button5 = InlineKeyboardButton(text='Мужской', callback_data='m')
in_button6 = InlineKeyboardButton(text='Женский', callback_data='w')

kb.add(in_button)
kb.add(in_button2)
kb2.add(in_button3)
kb2.add(in_button4)
kb3.add(in_button5)
kb3.add(in_button6)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать'),
         KeyboardButton(text='Информация')
         ]
    ], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью', reply_markup=start_menu)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберете опцию:', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def w_m(call):
    await call.message.answer('Укажите свой пол:', reply_markup=kb2)
    await call.answer()


@dp.callback_query_handler(text='female')
async def get_formula(call):
    await call.message.answer(f'10 x вес(кг) + 6,25 х рост(см) - 5 х возраст(лет) - 161')
    await call.answer()


@dp.callback_query_handler(text='male')
async def get_formula(call):
    await call.message.answer(f'10 x вес(кг) + 6,25 х рост(см) - 5 х возраст(лет) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def w_m(call):
    await call.message.answer('Укажите свой пол:', reply_markup=kb3)
    await call.answer()


@dp.callback_query_handler(text='w')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий: {norm} ')
    await state.finish()


@dp.callback_query_handler(text='m')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {norm} ')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
