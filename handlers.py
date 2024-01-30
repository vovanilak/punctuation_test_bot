from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F
from data import *
import keyboards
import random
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Этот бот предназначен для того, чтобы подтянуть твою пунктуацию. '
                         'Хочешь узнать свои знания? Используй /theme для выбора темы')

@router.message(Command('theme'))
async def cmd_theme(message: Message):
    await message.answer(text='Выбери правило',
                         reply_markup=keyboards.inline_builder(rules.keys()))

@router.message(Command('rules'))
async def cmd_tules(message: Message):
    await message.answer('')

@router.callback_query(F.data.in_(rules.keys()))
async def choose_rule(call: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    if info:
        rnd = random.choice(task[info['theme']])
    else:
        rnd = random.choice(task[call.data])
        await state.update_data(theme=call.data, dct=rnd)
    await call.message.answer(text=rnd['sent'],
                              reply_markup=keyboards.vars_key(rnd))
    await call.answer()

@router.callback_query(F.data.in_(('correct', 'incorrect')))
async def correct_answer(call: CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    theme = dct['theme']
    ask = dct['dct']
    rule = rules[theme][ask['rule']]
    if call.data == 'correct':
        await call.message.answer(f'Верно! А вот и правило:\n{rule}')
    else:
        await call.message.answer(f'Неверно( А вот почему:\n{rule}')
    await call.answer()
    await choose_rule(call, state)

@router.message()
async def main_error(message: Message):
    await message.answer('Что-то пошло не так. Используй /start чтобы перезапустить бота')

