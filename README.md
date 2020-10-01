# Reminder
###### Small practice in Heroku, schedules and configuration
Sends random message every day to do something - to take a pill or to water the flowers.

## Configuration
Project is Heroku-prepared with procfile and runtime.txt
### To specify message and target, use the following environment vars:
* telegram_api_token - token from bot_father, str
* bot_id - unused
* admin_id - id of user to send service messages, str
* target_id - id of user to send reminders, str
* messages - one or more messages to be chosen randomly, dot-separated, str
  * for instance - "msg1.msg2" or "msg1"
### By default, notification is sent once a day
#### To change it, modify schedule in main.py

## Is it alive?
* User with id matching admin_id can use command /notification_check to check if service alive
* Note: everyone knows that heroku instances can fall asleep if they do not receive traffic from outer internet, but it doesn't prevent them to send notification in time (in my case, at least)
