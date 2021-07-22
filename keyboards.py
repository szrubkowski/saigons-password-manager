from aiogram import types

import engine


class Keyboards:
    def __init__(self, name='', page=1):
        self.n_name = name
        self.n_page = page
        self.page_size = 10

    async def list_keyboard(self):
        # Возвращает список данных с бд
        pass_list = await engine.get_from_db(self.n_name)
        # Выделяет из списка нужную страницу
        pass_cut_list, temp_id = await engine.list_cut(self.n_page, self.page_size, pass_list)

        # Создаем клавиатуру и накидываем кнопки с базы
        keyboard_passwords_list = types.InlineKeyboardMarkup(row_width=3)
        for line in pass_cut_list:
            print('line: ', line)
            temp_id += 1
            button = types.KeyboardButton(text=str(temp_id) + ') ' + line[1],
                                          callback_data="inline_button_password-" + str(line[0]))
            keyboard_passwords_list.add(button)

        # Если полученный массив больше размера страницы - добавляем клавишы перемещения
        if len(pass_list) > self.page_size:
            print('inline_button_list-'+str(self.n_page))
            button_l = types.KeyboardButton(text='<', callback_data="inline_button_list-" + str(int(self.n_page) - 1))
            button_r = types.KeyboardButton(text='>', callback_data="inline_button_list-" + str(int(self.n_page) + 1))
            button_c = types.KeyboardButton(text=str(self.n_page), callback_data="inline_button_list-" + str(self.n_page))
            keyboard_passwords_list.add(button_l, button_c, button_r)

        return keyboard_passwords_list

    @staticmethod
    async def edit_keyboard(sql_index):
        keyboard_passwords_edit = types.InlineKeyboardMarkup(row_width=3)
        button_delete = types.KeyboardButton(text='❌ Удалить ❌', callback_data="inline_button_delete-" + str(sql_index))
        button_edit = types.KeyboardButton(text='✏️ Редактировать ✏️', callback_data="inline_button_edit-" + str(sql_index))
        button_hide = types.KeyboardButton(text='➖ Скрыть ➖', callback_data="inline_button_hide-" + str(sql_index))
        keyboard_passwords_edit.add(button_delete, button_edit, button_hide)
        return keyboard_passwords_edit
