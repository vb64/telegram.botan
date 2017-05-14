# pyTelegramBotAPI + appmetrica.yandex.ru botan
#
# pip install pyTelegramBotAPI
#
# from pyTelegramBotAPI_botan import Botan
#
# bot = Botan("telegram_bot_token", "metrica_api_token")
#
# set up 'start_prompt' function as handler for /start command in private chat
# every call of this handler automatically track to metrica with name='private.command.start'
#
# @bot.private_command("start")
# def start_prompt(message):
#     bot.reply_to(message, "Hello, private chat!")
#
# call member_left function when any member left group chat
# automatically track with name='group.left_chat_member'
#
# @bot.group_event("left_chat_member")
# def member_left(message):
#     bot.reply_to(message, "Oh, we lost him :(")
#
# set up 'member_help' function as handler for callback query in group chat,
# that contain "help_button_pressed" substring in callback_query.data
# automatically track with name='group.callback.help_button_pressed'
#
# @bot.group_callback("help_button_pressed")
# def member_help(message):
#     bot.reply_to(message, "Someone need help in our group!")
#
# available decorators:
#
# bot.private_command(command_name)
# bot.group_command(command_name)
# bot.private_event(content_type)
# bot.group_event(content_type)
# bot.private_callback(substring_in_callback_data)
# bot.group_callback(substring_in_callback_data)

from telebot import TeleBot
from botan import track as botan_track


def private_chat(message):
    return message.chat.type == "private"


def group_chat(message):
    return message.chat.type in ["group", "supergroup"]


class Botan(TeleBot):

    def __init__(self, telegram_token, metrica_token):
        TeleBot.__init__(self, telegram_token)
        self.metrica_token = metrica_token

    def track(self, event_name, message):
        botan_track(self.metrica_token, message.from_user.id, message, name=event_name)

    def callback_handler(self, metrica_prefix, command, func):

        def decorator(handler):

            def filter_func(call):
                return (func(call.message) and (command in call.data))

            def wrapper(call):
                self.track(metrica_prefix + '.' + command, call.message)
                return handler(call)

            self.add_callback_query_handler(self._build_handler_dict(
              wrapper,
              func=filter_func
            ))

        return decorator

    def private_callback(self, command):
        return self.callback_handler('private.callback', command, private_chat)

    def group_callback(self, command):
        return self.callback_handler('group.callback', command, group_chat)

    def update_handler(self, metrica_prefix, command, commands, content_types, func):

        def decorator(handler):

            def wrapper(message):
                self.track(metrica_prefix + '.' + command, message)
                return handler(message)

            self.add_message_handler(self._build_handler_dict(
              wrapper,
              commands=commands,
              regexp=None,
              func=func,
              content_types=content_types
            ))

            return wrapper

        return decorator

    def private_event(self, command):
        return self.update_handler('private', command, None, [command], private_chat)

    def group_event(self, command):
        return self.update_handler('group', command, None, [command], group_chat)

    def command_handler(self, metrica_prefix, command, func):
        return self.update_handler(metrica_prefix, command, [command], ['text'], func)

    def group_command(self, command):
        return self.command_handler('group.command', command, group_chat)

    def private_command(self, command):
        return self.command_handler('private.command', command, private_chat)
