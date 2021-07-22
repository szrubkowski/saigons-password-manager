from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import time

import config


def main():
    try:
        bot = Bot(token=config.token)
        dp = Dispatcher(bot)
        return bot, dp
    except:
        time.sleep(30)
