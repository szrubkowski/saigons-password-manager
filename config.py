import configparser

# Вытаскиваем данные из конфига
config = configparser.ConfigParser()
config.read("config.ini")

id_admin = config['Telegram']['id_admin']               # id аккаунта администратора
api_name = config['Telegram']['api_name']               # ник бота
token = config['Telegram']['token']                     # токен бота
database_name = config['Telegram']['database_name']     # название файла с базой данных

# Переменная add_mass нужна для процесса добавления нового пароля
add_mass = []      # Название, ник, эмайл, пароль, дополнительные ссылки, тэги
var_mass = []      # Сбор ID сообщений, которые необходимо удалить дабы не замусоривать бот
master_pass = ''   #
