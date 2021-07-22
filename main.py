#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from aiogram import types
from aiogram.utils import executor
from aiogram.types import ParseMode
import aiosqlite
import asyncio

import authorisation
import config
import engine
from keyboards import Keyboards
from db import SQL

# Авторизация бота в Телеграм
bot, dp = authorisation.main()


""" COMMANDS """


# Приветственное сообщение
@dp.message_handler(lambda message: str(message.chat.id) == config.id_admin,
                    lambda add_mass: config.add_mass == [], commands=['help', 'start'])
async def send_welcome(message: types.Message):
    print(message)
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(
        "🐉 Привет, используй следующие команды:\n\n"
        "/list - Список всех паролей\n"
        "/search *what* - Поиск пароля\n"
        "/create - Добавить пароль в базу\n"
    )


# Вывести список всех паролей в базе
@dp.message_handler(lambda message: str(message.chat.id) == config.id_admin,
                    lambda add_mass: config.add_mass == [], commands=['list'])
async def send_list(message: types.Message):
    show_list = Keyboards()
    data_list = await show_list.list_keyboard()
    await bot.delete_message(message.chat.id, message.message_id)
    if not data_list.inline_keyboard:
        await message.answer('🤷‍♂️Список пуст, введите /create, чтобы сохранить новый пароль.')
    else:
        await message.answer('🗒 Список паролей:', reply_markup=data_list)


# Вывести список всех паролей в базе по поиску
@dp.message_handler(lambda message: str(message.chat.id) == config.id_admin,
                    lambda add_mass: config.add_mass == [], commands=['search'])
async def send_list(message: types.Message):
    if len(message.text.split()) > 1:
        await bot.delete_message(message.chat.id, message.message_id)
        value_search = message.text.split()[1]
        show_list = Keyboards(value_search, 1)
        data_list = await show_list.list_keyboard()
        if not data_list.inline_keyboard:
            await message.answer('🤷‍♂️Список пуст, введите /create, чтобы сохранить новый пароль.')
        else:
            await message.answer(f'🗒 Список паролей по запросу <b>{value_search}</b>:',
                                 reply_markup=data_list, parse_mode=ParseMode.HTML)
    else:
        await message.answer(f'🗒 Укажите вместе с командой слово, по которому нужно поискать в списке',
                             parse_mode=ParseMode.HTML)


# Реакция на ввод команды create для создания новой записи в базе
@dp.message_handler(lambda message: str(message.chat.id) == config.id_admin,
                    lambda add_mass: config.add_mass == [], commands=['create'])
async def create_password(message: types.Message):
    message_temp = await message.answer(
        '🖋 Введи следующим сообщение название\nВведи /cancel, чтобы отменить добавление новой записи в базе')
    config.var_mass.append(message.message_id)
    config.var_mass.append(message_temp.message_id)

    for i in range(7):
        config.add_mass.append(False)


# Отмена добавления новой записи в базу
@dp.message_handler(lambda message: str(message.chat.id) == config.id_admin,
                    lambda add_mass: config.add_mass != [], commands=['cancel'])
async def cancel_creating(message: types.Message):
    temp = await message.answer('🚫 Добавление нового пароля в базу отменено')
    asyncio.create_task(engine.delete_message(temp.message_id, 30))

    for i in config.var_mass:
        await bot.delete_message(config.id_admin, i)

    config.add_mass = []
    config.id_admin = []


# Добавление новой записи в базу
@dp.message_handler(lambda message: str(message.chat.id) == config.id_admin,
                    lambda add_mass: config.add_mass != [])
async def send_list(message: types.Message):
    temp_text = ''
    if not config.add_mass[1]:
        config.add_mass[1] = message.text
        message_temp = await message.answer(
            f'📝 Название: <b>{message.text}</b>\nВведи никнейм или напиши \'none\', чтобы пропустить',
            parse_mode=ParseMode.HTML)
        config.var_mass.append(message.message_id)
        config.var_mass.append(message_temp.message_id)

    elif not config.add_mass[2]:
        config.add_mass[2] = message.text
        if message.text != 'none':
            temp_text = f'📝 Никнейм: <b>{message.text}</b>\n'

        message_temp = await message.answer(
            temp_text+'Введи email или напиши \'none\', чтобы пропустить этап',
            parse_mode=ParseMode.HTML)
        config.var_mass.append(message.message_id)
        config.var_mass.append(message_temp.message_id)

    elif not config.add_mass[3]:
        config.add_mass[3] = message.text
        if message.text != 'none':
            temp_text = f'📝 Email: <b>{message.text}</b>\n'

        message_temp = await message.answer(
            temp_text+'Введи пароль или напиши \'none\', чтобы пропустить этап',
            parse_mode=ParseMode.HTML)
        config.var_mass.append(message.message_id)
        config.var_mass.append(message_temp.message_id)

    elif not config.add_mass[4]:
        config.add_mass[4] = message.text
        if message.text != 'none':
            temp_text = f'📝 Пароль: <b>{message.text}</b>\n'

        message_temp = await message.answer(
            temp_text+'Введи ссылку или напиши \'none\', чтобы пропустить этап',
            parse_mode=ParseMode.HTML)
        config.var_mass.append(message.message_id)
        config.var_mass.append(message_temp.message_id)

    elif not config.add_mass[5]:
        config.add_mass[5] = message.text
        if message.text != 'none':
            temp_text = f'📝 Ссылка: <b>{message.text}</b>\n'

        message_temp = await message.answer(
            temp_text+'Введи тэги через запятую для спрощенного поиска или напиши \'none\', чтобы пропустить этап',
            parse_mode=ParseMode.HTML)
        config.var_mass.append(message.message_id)
        config.var_mass.append(message_temp.message_id)

    elif not config.add_mass[6]:
        config.add_mass[6] = message.text
        temp_text = '📝 Новая запись в базе:\n'
        temp_text += await engine.add_temp_text(config.add_mass)

        # Меняем значения где надо
        for i in config.add_mass:
            if i == 'none':
                config.add_mass[config.add_mass.index(i)] = None

        # Добавляем массив в базу данных
        hej = SQL()
        sql_index = await hej.create(config.add_mass)   # Получаем обратно местоположение записи в бд

        # Удаляем лишние сообщения
        config.var_mass.append(message.message_id)
        for i in config.var_mass:
            await bot.delete_message(config.id_admin, i)

        # Стираем массивы
        config.add_mass = []
        config.var_mass = []

        # Отправляем данные пользователю
        inline_edit_keyboard = await Keyboards.edit_keyboard(sql_index)
        await message.answer(temp_text, parse_mode=ParseMode.HTML, reply_markup=inline_edit_keyboard)


""" CALLBACK """


# Реакция бота при нажатии на кнопку в списке паролей
@dp.callback_query_handler(lambda c: 'inline_button_password' in c.data,
                           lambda add_mass: config.add_mass == [])
async def process_callback_keyboard_list(callback_query: types.CallbackQuery):
    # Отделяем от callback_query индекс
    index = int(callback_query.data.split('-')[1])

    # Получаем из базы информацию по конкретной ячейке
    async with aiosqlite.connect(config.database_name) as db:
        async with db.execute("SELECT * FROM {};".format('passwords_table')) as cursor:
            async for row in cursor:
                print(row, index)
                if int(row[0]) == index:
                    temp_text = await engine.add_temp_text(row)
                    inline_edit_keyboard = await Keyboards.edit_keyboard(int(row[0]))
                    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                    temp = await bot.send_message(callback_query.message.chat.id, temp_text,
                                                  parse_mode=ParseMode.HTML, reply_markup=inline_edit_keyboard)
                    asyncio.create_task(engine.delete_message(temp.message_id, 600))
                    

# Реакция бота на нажатие кнопок перелистывания страниц
@dp.callback_query_handler(lambda c: 'inline_button_list' in c.data,
                           lambda add_mass: config.add_mass == [])
async def process_callback_keyboard_page(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('-')[1])

    if index > 0:   # Бот не будет перелистывать на номера страниц, меньше за 1
        if callback_query.message.text == '🗒 Список паролей:':  # Если список со всеми паролями
            show_list = Keyboards('', index)
            data_list = await show_list.list_keyboard()
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.send_message(callback_query.message.chat.id, '🗒 Список паролей:', reply_markup=data_list)
        else:   # Если список с определённым запросом
            value_search = callback_query.message.text[len('🗒 Список паролей по запросу'):-1]
            print(value_search)
            show_list = Keyboards(value_search, index)
            data_list = await show_list.list_keyboard()
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.send_message(callback_query.message.chat.id, f'🗒 Список паролей по запросу <b>{value_search}</b>:', reply_markup=data_list)
    else:
        await callback_query.answer(text="Там ничего нет", show_alert=False)


# Реакция бота на нажатие кнопок скрытия
@dp.callback_query_handler(lambda c: 'inline_button_hide' in c.data,
                           lambda add_mass: config.add_mass == [])
async def process_callback_button_hide(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# Реакция бота на нажатие кнопки удалить
@dp.callback_query_handler(lambda c: 'inline_button_delete' in c.data,
                           lambda add_mass: config.add_mass == [])
async def process_callback_button_delete(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('-')[1])
    # print('DELETE INDEX:', index)
    hej = SQL()
    await hej.delete(index)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    temp = await bot.send_message(callback_query.message.chat.id, '🔥 Пароль удалён из базы')
    asyncio.create_task(engine.delete_message(temp.message_id, 30))


# Реакция бота на нажатие кнопки редактировать
@dp.callback_query_handler(lambda c: 'inline_button_edit' in c.data,
                           lambda add_mass: config.add_mass == [])
async def process_callback_button_edit(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('-')[1])
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(
        '🖋 Введи следующим сообщение название\nВведи /cancel, чтобы отменить редактирование записи в базе')
    config.add_mass.append(index)
    for i in range(6):
        config.add_mass.append(False)


""" OTHER """


# Если другой человек пытается использовать бот
@dp.message_handler(lambda message: str(message.chat.id) != config.id_admin)
async def whois(message: types.Message):
    print('WHOIS:', message)

if __name__ == '__main__':
    executor.start_polling(dp)
