# -*- coding: utf-8 -*-
import config
import telebot
import random
import schedule
import time
import threading
from telebot.types import Message

messages = config.messages
target_id = config.target_id
admin_id = config.admin_id
telegram_api_token = config.telegram_api_token

bot = telebot.TeleBot(telegram_api_token, threaded=True)


def notify():
    msg = random.choice(messages)
    try:
        bot.send_message(target_id, msg)
        bot.send_message(admin_id, "Цель получила напоминание")
        print("Message sent")
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, "Не получилось отправить напоминание")


@bot.message_handler(commands=["notification_check"])
def health_check(message: Message):
    if message.from_user.id == admin_id:
        print("Health check")
        bot.reply_to(message, text="Всё хорошо, напоминания работают")


def run_continuously(sched, interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                sched.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run



if __name__ == "__main__":
    print("Start serving")
    # bot.send_message(admin_id, "Модуль напоминаний готов")

    schedule.every().day.at("19:25").do(notify) #  -3 часа

    run_continuously(schedule)
    bot.polling()


