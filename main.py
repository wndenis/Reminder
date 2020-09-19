# -*- coding: utf-8 -*-
import config
import telebot
import random

from threading import Timer
from datetime import datetime, timedelta

messages = config.messages
target_id = config.target_id
admin_id = config.admin_id
telegram_api_token = config.telegram_api_token

bot = telebot.TeleBot(telegram_api_token)


def notify():
    msg = random.choice(messages)
    try:
        bot.send_message(target_id, msg)
        bot.send_message(admin_id, "Цель получила напоминание")
        print(messages)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, "Не получилось отправить напоминание")


class PerpetualTimer:
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.thread = Timer(self.interval, self.handle_function)

    def handle_function(self):
        self.function()
        self.thread = Timer(self.interval, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


if __name__ == "__main__":
    today_date = datetime.today()

    # next_date = today_date.replace(
    #     day=today_date.day, hour=22, minute=10, second=30, microsecond=0) + timedelta(days=1)
    # delta_t = next_date - today_date
    #
    # delta_t_secs = delta_t.total_seconds()
    delta_t_secs = 10
    t = PerpetualTimer(delta_t_secs, notify)
    t.start()
