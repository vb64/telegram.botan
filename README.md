# telegram.botan

[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) + [appmetrica.yandex.ru botan](https://github.com/botanio/sdk)

## Requirements

```
pip install pyTelegramBotAPI
wget https://raw.githubusercontent.com/botanio/sdk/master/botan.py
```

## Usage

```python
from pyTelegramBotAPI_botan import Botan

bot = Botan("telegram_bot_token", "metrica_api_token")
```

set up 'start_prompt' function as handler for /start command in private chat
every call of this handler automatically track to metrica with name='private.command.start'

```python
@bot.private_command("start")
def start_prompt(message):
    bot.reply_to(message, "Hello, private chat!")
```

set up 'member_left' function as handler for event, when any member left group chat
automatically track with name='group.left_chat_member'

```python
@bot.group_event("left_chat_member")
def member_left(message):
    bot.reply_to(message, "Oh, we lost him :(")
```

set up 'member_help' function as handler for callback query in group chat,
that contain "help_button_pressed" substring in callback_query.data
automatically track with name='group.callback.help_button_pressed'

```python
@bot.group_callback("help_button_pressed")
def member_help(call):
    bot.reply_to(call.message, "Someone need help in our group!")
```

available decorators:

```python
@bot.private_command(command_name)
@bot.group_command(command_name)
@bot.private_event(content_type)
@bot.group_event(content_type)
@bot.private_callback(substring_in_callback_data)
@bot.group_callback(substring_in_callback_data)
```
