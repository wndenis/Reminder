# -*- coding: utf-8 -*-

import os
telegram_api_token = os.environ['telegram_api_token']
bot_id = int(os.environ['bot_id'])
admin_id = int(os.environ['admin_id'])
target_id = int(os.environ['target_id'])
messages = [elem for elem in os.environ['messages'].split(".") if elem]

