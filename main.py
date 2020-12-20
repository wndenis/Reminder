# -*- coding: utf-8 -*-
import config
import telebot
import random
import schedule
import time
import threading
from telebot.types import Message
from facts import facts

messages = config.messages
target_id = config.target_id
admin_id = config.admin_id
telegram_api_token = config.telegram_api_token

bot = telebot.TeleBot(telegram_api_token, threaded=True)

do_notify = True
stopper = None
fact_id = random.randint(0, len(facts))

def notify():
    global do_notify
    if not do_notify:
        return
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

def enable_notifications():
    global do_notify
    if not do_notify:
        bot.send_message(admin_id, "Напоминания включены")
    do_notify = True

def disable_notifications():
    global do_notify
    if do_notify:
        bot.send_message(admin_id, "Напоминания выключены")
    do_notify = False

@bot.message_handler()
def general_messaging(message: Message):
    global do_notify, fact_id, stopper
    if message.from_user.id not in {admin_id, target_id}:
        return
    text = message.text.lower()
    stop_variants = ["пауз", "стоп", "останови", "отключи", "выключ", "не надо"]
    start_variants = ["восстанови", "продолж", "старт", "включ"]
    stop_verdict = max([elem in text for elem in stop_variants])
    start_verdict = max([elem in text for elem in start_variants])
    verdict = "ambiguous"
    if stop_verdict != start_verdict:
        if stop_verdict > start_verdict:
            verdict = "stop"
        else:
            verdict = "start"
    if verdict == "stop":
        if not do_notify:
            bot.reply_to(message, text="Уведомления были остановлены ранее")
            return
        if stopper is not None:
            stopper.abort()
        disable_notifications()
        stopper = run_delayed(enable_notifications, 60*60*24*6)
        bot.reply_to(message, text="Приостановила напоминания на 6 дней")
        return

    elif verdict == "start":
        if do_notify:
            bot.reply_to(message, text="Уведомления были включены ранее")
            return
        if stopper is not None:
            stopper.abort()
        enable_notifications()
        bot.reply_to(message, text="Включила напоминания")
        return

    ans = "Я пока не могу ничего другого, кроме уведомлений. Поэтому вот интересный факт:\n\n"
    ans += facts[fact_id]
    fact_id += 1
    if fact_id >= len(facts):
        fact_id = 0

    bot.reply_to(message, text=ans)


def run_continuously(sched, interval=2):
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


def run_delayed(func, delay=2):
    class ScheduleThread(threading.Thread):
        def __init__(self, func):
            super().__init__()
            self.func = func

        def run(self):
            time.sleep(delay)
            self.func()

        def abort(self):
            def idle():
                pass
            self.func = idle

    delayed_thread = ScheduleThread(func)
    delayed_thread.start()
    return delayed_thread


if __name__ == "__main__":
    print("Start serving")
    # bot.send_message(admin_id, "Модуль напоминаний готов")

    schedule.every().day.at("19:25").do(notify) #  -3 часа

    run_continuously(schedule)
    bot.polling()


