import aiosqlite
import asyncio
from Levenshtein import distance as lev

import config


async def get_from_db(name):       # Возвращает список данных с бд
    pass_list = []
    temp_k = 0

    async with aiosqlite.connect(config.database_name) as db:
        async with db.execute("SELECT * FROM {};".format('passwords_table')) as cursor:
            async for row in cursor:
                if name == '':      # Если нужно вывести весь список
                    temp_k += 1
                    pass_list.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                else:               # Вывести список по поиску
                    # Зависимость от расстояния Левенштайна между названием и поисковым запросом
                    if lev(row[1].lower(), name.lower()) < 4:
                        pass_list.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                    else:
                        # Зависимость от расстояния Левенштайна между тэгами и поисковым запросом
                        tags = row[6].split(',')
                        for tag in tags:
                            if lev(tag, name.lower()) < 4:
                                pass_list.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                                break
    return pass_list


async def list_cut(page, page_size, pass_list):    # Выделяет из списка нужную страницу
    print('l:', (page-1)*page_size, 'r:', (page*page_size))           # Дебаг
    pass_cut_list = pass_list[(page-1)*page_size:(page*page_size)]    # Обрезаем массив
    return pass_cut_list, (page-1)*page_size


async def add_temp_text(add_mass):
    temp_text = '\n<b>Название:</b> ' + add_mass[1]
    if add_mass[2] != 'none':
        temp_text += '\n<b>Никнейм:</b> ' + add_mass[2]
    if add_mass[3] != 'none':
        temp_text += '\n<b>Email:</b> ' + add_mass[3]
    if add_mass[4] != 'none':
        temp_text += '\n<b>Пароль:</b> ' + add_mass[4]
    if add_mass[5] != 'none':
        temp_text += '\n<b>Ссылка:</b> ' + add_mass[5]
    if add_mass[6] != 'none':
        temp_text += '\n<b>Тэги:</b> ' + add_mass[6]

    temp_text += ''

    return temp_text


async def delete_message(message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()
